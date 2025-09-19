"""
Unified_Media_Converter.py

Enhanced unified toolkit (audio + video) — professional, robust, single-file app.
Features combined and expanded from previous versions:
 - Load audio & video files; drag-and-drop support (optional tkinterdnd2)
 - Batch queue with start/stop, per-task progress and logs
 - Video -> audio extraction (MP3/AAC/FLAC/WAV/M4A) with advanced libmp3lame options (CBR/VBR)
 - Video -> video conversion (MP4/AVI/MKV/MOV) with quality/bitrate options
 - Audio -> audio conversion (MP3/AAC/FLAC/WAV/M4A) with quality/bitrate options
 - Parametric EQ editor (parametric/highpass/lowpass bands) with per-band mute/solo/invert
 - Preview with FFmpeg filter or linear-phase FIR (design + overlap-add convolution)
 - Final export options: FFmpeg filter chain or exact linear-phase FIR convolution
 - Export FIR coefficients (CSV, .f32 raw, IR WAV for FFmpeg afir)
 - A/B compare and instant crossfade audition between A and B
 - Real-time FFmpeg progress parsing and GUI updates
 - Presets (save/load) and per-band presets
 - UI polish: drag/drop hotspots, keyboard shortcuts, disabled controls during processing
 - Robust threading, queue-based UI updates, and defensive error handling

Requirements:
 - Python 3.8+
 - ffmpeg and ffprobe in PATH
 - Optional but recommended: pip install numpy matplotlib simpleaudio tkinterdnd2

Save as unified_media_converter.py and run:
    python unified_media_converter.py

"""
from __future__ import annotations

import os
import sys
import json
import shutil
import tempfile
import threading
import subprocess
import math
import queue
import time
import traceback
import wave
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Tuple

# GUI
try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
except Exception as e:
    raise RuntimeError('Tkinter required')

# Optional drag-and-drop
DND_AVAILABLE = False
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except Exception:
    DND_AVAILABLE = False

# Optional libs
NP_AVAILABLE = True
MATPLOTLIB_AVAILABLE = True
FigureCanvasTkAgg = None
Figure = None
try:
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
except Exception:
    NP_AVAILABLE = False
    MATPLOTLIB_AVAILABLE = False
    FigureCanvasTkAgg = None
    Figure = None

SIMPLEAUDIO_AVAILABLE = True
try:
    import simpleaudio as sa
except Exception:
    SIMPLEAUDIO_AVAILABLE = False

# Constants
APP_TITLE = 'Unified Media Converter v7'
PRESETS_FILE = Path.home() / '.umc_presets.json'
PREVIEW_DURATION = 6
LOG_MAX_LINES = 3000

# Media format constants
VIDEO_FORMATS = ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm']
AUDIO_FORMATS = ['mp3', 'aac', 'flac', 'wav', 'm4a', 'ogg', 'wma']
ALL_FORMATS = VIDEO_FORMATS + AUDIO_FORMATS

# ---------------- Data classes ----------------
@dataclass
class Band:
    type: str = 'parametric'  # parametric | highpass | lowpass
    f: float = 1000.0
    width_type: str = 'q'     # q | oct
    width: float = 1.0
    g: float = 0.0
    muted: bool = False
    solo: bool = False
    invert: bool = False

    def copy(self) -> 'Band':
        return Band(**asdict(self))

@dataclass
class Task:
    input_path: str
    output_path: str
    action: str  # 'apply_eq', 'extract_audio', 'convert_video', 'convert_audio', 'noop'
    options: Dict[str, Any]
    id: Optional[str] = None

# ---------------- Utilities ----------------
import shlex

def which_exe(name: str) -> Optional[str]:
    return shutil.which(name)

def ffprobe_duration(path: str) -> float:
    ffprobe = which_exe('ffprobe')
    if ffprobe is None:
        return 0.0
    cmd = [ffprobe, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', path]
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        return float(out.decode().strip())
    except Exception:
        return 0.0

def get_file_type(path: str) -> str:
    """Determine if file is audio or video based on extension"""
    ext = Path(path).suffix.lower().lstrip('.')
    if ext in VIDEO_FORMATS:
        return 'video'
    elif ext in AUDIO_FORMATS:
        return 'audio'
    return 'unknown'

def get_media_info(path: str) -> Dict[str, Any]:
    """Get detailed media information using ffprobe"""
    ffprobe = which_exe('ffprobe')
    if ffprobe is None:
        return {}
    
    # Get format info
    cmd = [ffprobe, '-v', 'error', '-show_entries', 
           'format=duration,size,bit_rate,format_name', 
           '-of', 'default=noprint_wrappers=1', path]
    
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
        info = {}
        for line in out.decode().strip().split('\n'):
            if '=' in line:
                k, v = line.split('=', 1)
                info[k] = v
        return info
    except Exception:
        return {}

# ---------------- DSP & FIR helpers ----------------
if NP_AVAILABLE:
    import cmath
    import numpy as np

    def peaking_eq_response(band: Band, freqs: np.ndarray, fs: float) -> np.ndarray:
        f0 = float(max(1.0, min(band.f, fs/2 - 1)))
        G = 10**(band.g / 40.0)
        if band.width_type == 'q':
            Q = max(0.01, float(band.width))
        else:
            bw = max(0.001, float(band.width))
            f2 = f0 * (2**(bw/2))
            f1 = f0 / (2**(bw/2))
            denom = (f2 - f1)
            Q = f0 / denom if denom > 1e-12 else 1.0
        w0 = 2 * math.pi * f0 / fs
        cosw0 = math.cos(w0); sinw0 = math.sin(w0)
        alpha = sinw0 / (2 * Q)
        b0 = 1 + alpha * G
        b1 = -2 * cosw0
        b2 = 1 - alpha * G
        a0 = 1 + alpha / G
        a1 = -2 * cosw0
        a2 = 1 - alpha / G
        ws = 2 * math.pi * freqs / fs
        z1 = np.exp(-1j * ws)
        z2 = np.exp(-2j * ws)
        num = b0 + b1 * z1 + b2 * z2
        den = a0 + a1 * z1 + a2 * z2
        H = num / den
        if band.invert:
            H = -H
        return H

    def lowpass_response(fc: float, freqs: np.ndarray, fs: float) -> np.ndarray:
        Q = 1 / math.sqrt(2)
        w0 = 2 * math.pi * fc / fs
        cosw0 = np.cos(w0); sinw0 = np.sin(w0)
        alpha = sinw0 / (2 * Q)
        b0 = (1 - cosw0) / 2
        b1 = 1 - cosw0
        b2 = (1 - cosw0) / 2
        a0 = 1 + alpha
        a1 = -2 * cosw0
        a2 = 1 - alpha
        ws = 2 * math.pi * freqs / fs
        z1 = np.exp(-1j * ws)
        z2 = np.exp(-2j * ws)
        H = (b0 + b1 * z1 + b2 * z2) / (a0 + a1 * z1 + a2 * z2)
        return H

    def highpass_response(fc: float, freqs: np.ndarray, fs: float) -> np.ndarray:
        Q = 1 / math.sqrt(2)
        w0 = 2 * math.pi * fc / fs
        cosw0 = np.cos(w0); sinw0 = np.sin(w0)
        alpha = sinw0 / (2 * Q)
        b0 = (1 + cosw0) / 2
        b1 = -(1 + cosw0)
        b2 = (1 + cosw0) / 2
        a0 = 1 + alpha
        a1 = -2 * cosw0
        a2 = 1 - alpha
        ws = 2 * math.pi * freqs / fs
        z1 = np.exp(-1j * ws)
        z2 = np.exp(-2j * ws)
        H = (b0 + b1 * z1 + b2 * z2) / (a0 + a1 * z1 + a2 * z2)
        return H

    def compute_total_response(bands: List[Band], freqs: np.ndarray, fs: float) -> np.ndarray:
        H_total = np.ones_like(freqs, dtype=complex)
        for b in bands:
            if b.type == 'parametric':
                H = peaking_eq_response(b, freqs, fs)
            elif b.type == 'lowpass':
                H = lowpass_response(b.f, freqs, fs)
            elif b.type == 'highpass':
                H = highpass_response(b.f, freqs, fs)
            else:
                H = np.ones_like(freqs, dtype=complex)
            H_total *= H
        return H_total

    def design_linear_phase_fir(bands: List[Band], fs: int, n_taps: int = 2048) -> np.ndarray:
        if n_taps % 2 != 0:
            n_taps += 1
        n_freq = n_taps
        freqs = np.linspace(0, fs/2, n_freq//2 + 1)
        H_pos = compute_total_response(bands, freqs, fs)
        full = np.concatenate([H_pos, np.conj(H_pos[-2:0:-1])])
        h = np.fft.ifft(full)
        h = np.real(h)
        win = np.hanning(len(h))
        h = h * win
        s = np.sum(h)
        if abs(s) > 1e-12:
            h /= s
        return h[:n_taps]

    def next_pow2(x: int) -> int:
        return 1 << (x - 1).bit_length()

    def overlap_add_convolve_wav(in_wav: str, fir: np.ndarray, out_wav: str, block_size: int = 65536, ui_queue: Optional[queue.Queue] = None, task_id: Optional[str] = None):
        with wave.open(in_wav, 'rb') as wf_in:
            nch = wf_in.getnchannels(); sr = wf_in.getframerate(); sw = wf_in.getsampwidth(); nframes = wf_in.getnframes()
            if sw != 2:
                raise RuntimeError('Only 16-bit PCM supported for internal convolution')
            with wave.open(out_wav, 'wb') as wf_out:
                wf_out.setnchannels(nch); wf_out.setsampwidth(2); wf_out.setframerate(sr)
                Lh = len(fir)
                N = next_pow2(block_size + Lh - 1)
                H = np.fft.rfft(fir, n=N)
                overlap = np.zeros((Lh - 1, nch), dtype=np.float64)
                total_frames = nframes
                processed = 0
                while True:
                    frames = wf_in.readframes(block_size)
                    if not frames:
                        break
                    data = np.frombuffer(frames, dtype=np.int16).astype(np.float64).reshape(-1, nch)
                    m = data.shape[0]
                    Y = np.zeros((N, nch), dtype=np.float64)
                    for ch in range(nch):
                        x = data[:, ch]
                        X = np.fft.rfft(x, n=N)
                        y = np.fft.irfft(X * H, n=N)
                        Y[:, ch] = y
                    out_block = Y[:m, :] + overlap[:m, :]
                    out_block_clamped = np.clip(out_block, -32767, 32767).astype(np.int16)
                    wf_out.writeframes(out_block_clamped.tobytes())
                    overlap_new = Y[m:m + (Lh - 1), :]
                    if overlap_new.shape[0] < (Lh - 1):
                        pad = np.zeros(((Lh - 1) - overlap_new.shape[0], nch), dtype=np.float64)
                        overlap = np.vstack([overlap_new, pad])
                    else:
                        overlap = overlap_new
                    processed += m
                    if ui_queue and task_id:
                        pct = min(100.0, (processed / total_frames) * 100.0)
                        ui_queue.put(('progress', (task_id, pct)))
                tail = overlap
                if tail.shape[0] > 0:
                    tail_clamped = np.clip(tail, -32767, 32767).astype(np.int16)
                    wf_out.writeframes(tail_clamped.tobytes())
                if ui_queue and task_id:
                    ui_queue.put(('progress', (task_id, 100.0)))

# ---------------- FFmpeg worker (generalized for audio/video tasks) ----------------
class Worker(threading.Thread):
    def __init__(self, task: Task, bands: List[Band], ui_queue: queue.Queue):
        super().__init__(daemon=True)
        self.task = task
        self.bands = bands
        self.ui_queue = ui_queue
        self._proc = None

    def run(self):
        try:
            if self.task.action == 'apply_eq':
                self._apply_eq()
            elif self.task.action == 'extract_audio':
                self._extract_audio()
            elif self.task.action == 'convert_video':
                self._convert_video()
            elif self.task.action == 'convert_audio':
                self._convert_audio()
            else:
                self.ui_queue.put(('log', f'Unknown task action {self.task.action}'))
        except Exception as e:
            self.ui_queue.put(('error', f'Worker exception: {e}\n{traceback.format_exc()}'))
        finally:
            self.ui_queue.put(('done', self.task.id))

    def _run_cmd_with_progress(self, cmd: List[str], input_path: Optional[str] = None):
        duration = ffprobe_duration(input_path) if input_path else 0.0
        self.ui_queue.put(('cmd', ' '.join(shlex.quote(c) for c in cmd)))
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            self._proc = proc
            last_pct = 0.0
            for line in proc.stdout:
                line = line.strip()
                self.ui_queue.put(('log', line))
                t = None
                if 'time=' in line:
                    t = parse_ffmpeg_time(line)
                if t is not None and duration > 0:
                    pct = min(100.0, (t / duration) * 100.0)
                    if pct - last_pct >= 0.5 or pct == 100.0:
                        last_pct = pct
                        self.ui_queue.put(('progress', (self.task.id, pct)))
            rc = proc.wait()
            if rc != 0:
                self.ui_queue.put(('error', f'ffmpeg returned {rc}'))
            else:
                self.ui_queue.put(('progress', (self.task.id, 100.0)))
        except Exception as e:
            self.ui_queue.put(('error', f'ffmpeg error: {e}'))

    def _apply_eq(self):
        opt = self.task.options
        use_fir = opt.get('use_fir', False)
        sr = opt.get('sr', 44100)
        ch = opt.get('ch', 2)
        fmt = opt.get('format', 'wav')
        if not use_fir:
            filters = build_ffmpeg_filter(self.bands)
            cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', self.task.input_path]
            if filters:
                cmd += ['-af', filters]
            if fmt == 'mp3':
                cmd += ['-ar', str(sr), '-ac', str(ch), '-c:a', 'libmp3lame', '-b:a', opt.get('mp3_bitrate', '192k'), self.task.output_path]
            elif fmt == 'flac':
                cmd += ['-ar', str(sr), '-ac', str(ch), '-c:a', 'flac', self.task.output_path]
            elif fmt == 'aac':
                cmd += ['-ar', str(sr), '-ac', str(ch), '-c:a', 'aac', '-b:a', opt.get('aac_bitrate', '192k'), self.task.output_path]
            else:
                cmd += ['-ar', str(sr), '-ac', str(ch), '-c:a', 'pcm_s16le', self.task.output_path]
            self._run_cmd_with_progress(cmd, self.task.input_path)
        else:
            # FIR pipeline: decode -> convolve -> encode
            if not NP_AVAILABLE:
                self.ui_queue.put(('error', 'numpy required for FIR export'))
                return
            tmp_dec = os.path.join(tempfile.gettempdir(), f'umc_dec_{int(time.time())}.wav')
            tmp_conv = os.path.join(tempfile.gettempdir(), f'umc_conv_{int(time.time())}.wav')
            # decode
            cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', self.task.input_path, '-ar', str(sr), '-ac', str(ch), '-c:a', 'pcm_s16le', tmp_dec]
            rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if rc != 0:
                self.ui_queue.put(('error', 'ffmpeg decode failed for FIR path'))
                return
            # design FIR
            n_taps = int(opt.get('n_taps', 2048))
            self.ui_queue.put(('log', f'Designing FIR ({n_taps} taps)'))
            fir = design_linear_phase_fir(self.bands, sr, n_taps)
            # convolve
            self.ui_queue.put(('log', 'Starting overlap-add convolution'))
            try:
                overlap_add_convolve_wav(tmp_dec, fir, tmp_conv, block_size=65536, ui_queue=self.ui_queue, task_id=self.task.id)
            except Exception as e:
                self.ui_queue.put(('error', f'Convolution failed: {e}'))
                return
            # encode
            if fmt == 'mp3':
                cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_conv, '-ar', str(sr), '-ac', str(ch), '-c:a', 'libmp3lame', '-b:a', opt.get('mp3_bitrate', '192k'), self.task.output_path]
            elif fmt == 'flac':
                cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_conv, '-ar', str(sr), '-ac', str(ch), '-c:a', 'flac', self.task.output_path]
            elif fmt == 'aac':
                cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_conv, '-ar', str(sr), '-ac', str(ch), '-c:a', 'aac', '-b:a', opt.get('aac_bitrate', '192k'), self.task.output_path]
            else:
                # wav destination -> move tmp_conv
                try:
                    shutil.move(tmp_conv, self.task.output_path)
                    tmp_conv = None
                except Exception as e:
                    self.ui_queue.put(('error', f'Failed move WAV: {e}'))
                    return
            if tmp_conv and os.path.exists(tmp_conv):
                rc = subprocess.call(cmd)
                if rc != 0:
                    self.ui_queue.put(('error', 'ffmpeg re-encode failed after FIR'))
                    return
            # cleanup
            try:
                if os.path.exists(tmp_dec): os.remove(tmp_dec)
            except Exception:
                pass
            try:
                if tmp_conv and os.path.exists(tmp_conv): os.remove(tmp_conv)
            except Exception:
                pass
            self.ui_queue.put(('log', f'FIR export complete: {self.task.output_path}'))

    def _extract_audio(self):
        opt = self.task.options
        fmt = opt.get('format', 'wav')
        sr = opt.get('sr', 44100)
        ch = opt.get('ch', 2)
        cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', self.task.input_path, '-vn', '-ar', str(sr), '-ac', str(ch)]
        if fmt == 'mp3':
            cmd += ['-c:a', 'libmp3lame', '-b:a', opt.get('mp3_bitrate','192k'), self.task.output_path]
        elif fmt == 'flac':
            cmd += ['-c:a', 'flac', self.task.output_path]
        elif fmt == 'aac':
            cmd += ['-c:a', 'aac', '-b:a', opt.get('aac_bitrate','192k'), self.task.output_path]
        else:
            cmd += ['-c:a', 'pcm_s16le', self.task.output_path]
        self._run_cmd_with_progress(cmd, self.task.input_path)

    def _convert_video(self):
        """Convert video file to another video format with quality options"""
        opt = self.task.options
        fmt = opt.get('format', 'mp4')
        video_codec = opt.get('video_codec', 'libx264')
        audio_codec = opt.get('audio_codec', 'aac')
        video_bitrate = opt.get('video_bitrate', '1000k')
        audio_bitrate = opt.get('audio_bitrate', '128k')
        
        cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', self.task.input_path]
        
        # Video codec and quality
        if video_codec == 'libx264':
            cmd += ['-c:v', 'libx264', '-b:v', video_bitrate, '-preset', 'medium']
        elif video_codec == 'libx265':
            cmd += ['-c:v', 'libx265', '-b:v', video_bitrate, '-preset', 'medium']
        elif video_codec == 'vp9':
            cmd += ['-c:v', 'libvpx-vp9', '-b:v', video_bitrate]
        else:
            cmd += ['-c:v', 'copy']  # Copy video stream if no re-encoding needed
            
        # Audio codec and quality
        if audio_codec == 'aac':
            cmd += ['-c:a', 'aac', '-b:a', audio_bitrate]
        elif audio_codec == 'mp3':
            cmd += ['-c:a', 'libmp3lame', '-b:a', audio_bitrate]
        elif audio_codec == 'flac':
            cmd += ['-c:a', 'flac']
        else:
            cmd += ['-c:a', 'copy']  # Copy audio stream if no re-encoding needed
            
        cmd.append(self.task.output_path)
        self._run_cmd_with_progress(cmd, self.task.input_path)

    def _convert_audio(self):
        """Convert audio file to another audio format with quality options"""
        opt = self.task.options
        fmt = opt.get('format', 'wav')
        sr = opt.get('sr', 44100)
        ch = opt.get('ch', 2)
        
        cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', self.task.input_path, '-ar', str(sr), '-ac', str(ch)]
        
        if fmt == 'mp3':
            cmd += ['-c:a', 'libmp3lame', '-b:a', opt.get('mp3_bitrate','192k'), self.task.output_path]
        elif fmt == 'flac':
            cmd += ['-c:a', 'flac', self.task.output_path]
        elif fmt == 'aac':
            cmd += ['-c:a', 'aac', '-b:a', opt.get('aac_bitrate','192k'), self.task.output_path]
        elif fmt == 'ogg':
            cmd += ['-c:a', 'libvorbis', '-b:a', opt.get('ogg_bitrate','128k'), self.task.output_path]
        else:
            cmd += ['-c:a', 'pcm_s16le', self.task.output_path]
            
        self._run_cmd_with_progress(cmd, self.task.input_path)

# Helper parse time

def parse_ffmpeg_time(line: str) -> Optional[float]:
    if 'time=' not in line:
        return None
    try:
        seg = line.split('time=')[1].split(' ')[0]
        parts = seg.split(':')
        if len(parts) == 3:
            h, m, s = parts
            return float(h) * 3600 + float(m) * 60 + float(s)
        return float(seg)
    except Exception:
        return None

# Build ffmpeg filter

def build_ffmpeg_filter(bands: List[Band]) -> str:
    pieces = []
    for b in bands:
        if b.type == 'highpass':
            pieces.append(f'highpass=f={int(b.f)}')
        elif b.type == 'lowpass':
            pieces.append(f'lowpass=f={int(b.f)}')
        else:
            wtype = 'q' if b.width_type == 'q' else 'oct'
            pieces.append(f'equalizer=f={int(b.f)}:width_type={wtype}:width={b.width:g}:g={b.g:g}')
    return ','.join(pieces)

# ---------------- GUI Application ----------------
class UnifiedApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry('1320x820')
        self.ui_queue: queue.Queue = queue.Queue()
        self._tasks: List[Task] = []
        self._workers: Dict[str, Worker] = {}
        self.bands: List[Band] = []
        self.ab_a: Optional[List[Band]] = None
        self.ab_b: Optional[List[Band]] = None
        self._play_obj = None

        self._build_ui()
        self._load_presets()
        self._build_default_bands()
        self._start_ui_loop()

    def _build_ui(self):
        # Top toolbar
        top = ttk.Frame(self.root, padding=6)
        top.pack(side='top', fill='x')
        ttk.Button(top, text='Add Files', command=self.add_files).pack(side='left')
        ttk.Button(top, text='Add Folder', command=self.add_folder).pack(side='left')
        ttk.Button(top, text='Start Queue', command=self.start_queue).pack(side='left', padx=6)
        ttk.Button(top, text='Stop All', command=self.stop_all).pack(side='left')
        ttk.Button(top, text='Save Preset', command=self.save_preset).pack(side='right')
        ttk.Button(top, text='Load Preset', command=self.load_preset).pack(side='right', padx=4)
        ttk.Button(top, text='Save FIR Coeffs', command=self.export_fir_coeffs_dialog).pack(side='right', padx=8)

        self.status_var = tk.StringVar(value='Idle')
        ttk.Label(top, textvariable=self.status_var, relief='sunken', anchor='w', width=80).pack(side='right', padx=6)

        main = ttk.PanedWindow(self.root, orient='horizontal')
        main.pack(fill='both', expand=True)

        left = ttk.Frame(main)
        main.add(left, weight=2)
        mid = ttk.Frame(main)
        main.add(mid, weight=2)
        right = ttk.Frame(main)
        main.add(right, weight=1)

        # Left: queue/task list
        lf = ttk.LabelFrame(left, text='Task Queue')
        lf.pack(fill='both', expand=True, padx=6, pady=6)
        self.task_tree = ttk.Treeview(lf, columns=('action','status','progress'), show='headings', height=12)
        self.task_tree.heading('action', text='Action')
        self.task_tree.heading('status', text='Status')
        self.task_tree.heading('progress', text='Progress')
        self.task_tree.pack(fill='both', expand=True)
        tk.Label(lf, text='Double-click a task to create an export task from an input file').pack()
        self.task_tree.bind('<Double-1>', self._on_task_double)

        # Middle: EQ editor and bands
        eqf = ttk.LabelFrame(mid, text='Parametric EQ Editor')
        eqf.pack(fill='both', expand=True, padx=6, pady=6)
        ctrl = ttk.Frame(eqf)
        ctrl.pack(fill='x')
        ttk.Button(ctrl, text='Add Band', command=self.add_band).pack(side='left')
        ttk.Button(ctrl, text='Reset', command=self._build_default_bands).pack(side='left', padx=4)
        ttk.Button(ctrl, text='Save A', command=self.save_ab_a).pack(side='right')
        ttk.Button(ctrl, text='Save B', command=self.save_ab_b).pack(side='right', padx=4)
        ttk.Button(ctrl, text='Toggle A/B', command=self.toggle_ab).pack(side='right', padx=4)

        self.band_container = ttk.Frame(eqf)
        self.band_container.pack(fill='both', expand=True)

        # Right: visualiser, preview, logs
        vizf = ttk.LabelFrame(right, text='Visualizer & Preview')
        vizf.pack(fill='both', expand=True, padx=6, pady=6)
        if MATPLOTLIB_AVAILABLE and NP_AVAILABLE:
            self.figure = Figure(figsize=(5,3), dpi=120)
            self.ax = self.figure.add_subplot(111)
            self.canvas_fig = FigureCanvasTkAgg(self.figure, master=vizf)
            self.canvas_fig.get_tk_widget().pack(fill='both', expand=True)
        else:
            ttk.Label(vizf, text='Install numpy+matplotlib for visualiser').pack(padx=6, pady=6)

        pvf = ttk.Frame(right)
        pvf.pack(fill='x')
        ttk.Button(pvf, text='Render & Play Preview', command=self.preview_choice_threaded).pack(side='left')
        ttk.Button(pvf, text='A/B Crossfade', command=self.ab_crossfade_threaded).pack(side='left', padx=6)
        ttk.Button(pvf, text='Export Visual (PNG)', command=self.export_visual_png).pack(side='right')
        ttk.Button(pvf, text='Export Visual (CSV)', command=self.export_visual_csv).pack(side='right', padx=4)

        logf = ttk.LabelFrame(right, text='Logs')
        logf.pack(fill='both', expand=True, padx=6, pady=6)
        self.log_text = tk.Text(logf, height=12)
        self.log_text.pack(fill='both', expand=True)

        self.global_progress = ttk.Progressbar(self.root, orient='horizontal', length=1000, mode='determinate')
        self.global_progress.pack(side='bottom', pady=6)

        # Keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.add_files())
        self.root.bind('<Control-s>', lambda e: self.save_preset())

        # Drag-and-drop support area
        if DND_AVAILABLE:
            ddf = ttk.Label(self.root, text='Drag & Drop files here', relief='ridge', padding=6)
            ddf.pack(side='bottom', fill='x')
            ddf.drop_target_register(DND_FILES)
            ddf.dnd_bind('<<Drop>>', self._on_drop)

    # ---------------- Task queue management ----------------
    def add_files(self):
        paths = filedialog.askopenfilenames(title='Select files (audio or video)')
        for p in paths:
            self._add_file_to_queue(p)

    def add_folder(self):
        folder = filedialog.askdirectory(title='Select folder')
        if not folder:
            return
        for root, dirs, files in os.walk(folder):
            for f in files:
                if Path(f).suffix.lower().lstrip('.') in ALL_FORMATS:
                    self._add_file_to_queue(os.path.join(root, f))

    def _add_file_to_queue(self, path: str):
        tid = str(time.time()) + os.path.basename(path)
        t = Task(input_path=path, output_path='', action='pending', options={}, id=tid)
        self._tasks.append(t)
        self._refresh_task_tree()
        self.log(f'Queued: {path}')

    def _refresh_task_tree(self):
        for iid in self.task_tree.get_children():
            self.task_tree.delete(iid)
        for t in self._tasks:
            status = t.action
            prog = '0%'
            self.task_tree.insert('', 'end', iid=t.id, values=(status, '', prog))

    def _on_task_double(self, event):
        sel = self.task_tree.selection()
        if not sel:
            return
        iid = sel[0]
        # find task
        for t in self._tasks:
            if t.id == iid:
                # Determine file type and offer appropriate conversion options
                file_type = get_file_type(t.input_path)
                
                # Create export dialog
                self._create_export_dialog(t)
                return

    def _create_export_dialog(self, task: Task):
        """Create a dialog for export options based on file type"""
        file_type = get_file_type(task.input_path)
        
        # Create export dialog window
        export_win = tk.Toplevel(self.root)
        export_win.title(f"Export Options - {Path(task.input_path).name}")
        export_win.geometry("500x400")
        export_win.transient(self.root)
        export_win.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(export_win, padding=10)
        main_frame.pack(fill='both', expand=True)
        
        # Output format selection
        fmt_frame = ttk.LabelFrame(main_frame, text="Output Format", padding=10)
        fmt_frame.pack(fill='x', pady=5)
        
        fmt_var = tk.StringVar()
        if file_type == 'video':
            formats = ['mp4', 'avi', 'mkv', 'mov', 'mp3', 'aac', 'flac', 'wav']
        else:  # audio
            formats = ['mp3', 'aac', 'flac', 'wav', 'm4a', 'ogg']
            
        fmt_var.set(formats[0])
        fmt_combo = ttk.Combobox(fmt_frame, textvariable=fmt_var, values=formats, state='readonly')
        fmt_combo.pack(side='left')
        
        # Output file selection
        out_frame = ttk.Frame(main_frame)
        out_frame.pack(fill='x', pady=5)
        
        ttk.Label(out_frame, text="Output File:").pack(side='left')
        out_var = tk.StringVar()
        out_entry = ttk.Entry(out_frame, textvariable=out_var, width=40)
        out_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        browse_btn = ttk.Button(out_frame, text="Browse...", 
                               command=lambda: self._browse_output_file(fmt_var.get(), out_var))
        browse_btn.pack(side='left', padx=5)
        
        # Update output entry when format changes
        def update_output(*args):
            base = Path(task.input_path).stem
            ext = fmt_var.get()
            out_var.set(filedialog.asksaveasfilename(
                initialfile=f"{base}.{ext}",
                defaultextension=f".{ext}",
                filetypes=[(f"{ext.upper()} files", f"*.{ext}")]
            ))
        
        fmt_var.trace('w', update_output)
        
        # Quality options frame
        quality_frame = ttk.LabelFrame(main_frame, text="Quality Options", padding=10)
        quality_frame.pack(fill='both', expand=True, pady=5)
        
        # Sample rate and channels
        sr_frame = ttk.Frame(quality_frame)
        sr_frame.pack(fill='x', pady=2)
        ttk.Label(sr_frame, text="Sample Rate (Hz):").pack(side='left')
        sr_var = tk.StringVar(value="44100")
        sr_combo = ttk.Combobox(sr_frame, textvariable=sr_var, 
                               values=["8000", "11025", "12000", "16000", "22050", "24000", "32000", "44100", "48000"], width=10)
        sr_combo.pack(side='left', padx=5)
        
        ch_frame = ttk.Frame(quality_frame)
        ch_frame.pack(fill='x', pady=2)
        ttk.Label(ch_frame, text="Channels:").pack(side='left')
        ch_var = tk.StringVar(value="2")
        ch_combo = ttk.Combobox(ch_frame, textvariable=ch_var, 
                               values=["1", "2"], width=10)
        ch_combo.pack(side='left', padx=5)
        
        # Bitrate options (shown based on format)
        bitrate_frame = ttk.Frame(quality_frame)
        bitrate_frame.pack(fill='x', pady=2)
        ttk.Label(bitrate_frame, text="Bitrate:").pack(side='left')
        bitrate_var = tk.StringVar(value="192k")
        bitrate_combo = ttk.Combobox(bitrate_frame, textvariable=bitrate_var, 
                                    values=["64k", "128k", "192k", "256k", "320k"], width=10)
        bitrate_combo.pack(side='left', padx=5)
        
        # Initialize video-specific variables with default values
        vcodec_var = tk.StringVar(value="libx264")
        vbitrate_var = tk.StringVar(value="1000k")
        acodec_var = tk.StringVar(value="aac")
        
        # Video-specific options
        if file_type == 'video':
            # Video codec
            vcodec_frame = ttk.Frame(quality_frame)
            vcodec_frame.pack(fill='x', pady=2)
            ttk.Label(vcodec_frame, text="Video Codec:").pack(side='left')
            vcodec_combo = ttk.Combobox(vcodec_frame, textvariable=vcodec_var,
                                       values=["libx264", "libx265", "copy"], width=10)
            vcodec_combo.pack(side='left', padx=5)
            
            # Video bitrate
            vbitrate_frame = ttk.Frame(quality_frame)
            vbitrate_frame.pack(fill='x', pady=2)
            ttk.Label(vbitrate_frame, text="Video Bitrate:").pack(side='left')
            vbitrate_combo = ttk.Combobox(vbitrate_frame, textvariable=vbitrate_var,
                                         values=["500k", "1000k", "2000k", "4000k"], width=10)
            vbitrate_combo.pack(side='left', padx=5)
            
            # Audio codec for video
            acodec_frame = ttk.Frame(quality_frame)
            acodec_frame.pack(fill='x', pady=2)
            ttk.Label(acodec_frame, text="Audio Codec:").pack(side='left')
            acodec_combo = ttk.Combobox(acodec_frame, textvariable=acodec_var,
                                       values=["aac", "mp3", "flac", "copy"], width=10)
            acodec_combo.pack(side='left', padx=5)
        
        # EQ options
        eq_frame = ttk.LabelFrame(main_frame, text="EQ Processing", padding=10)
        eq_frame.pack(fill='x', pady=5)
        
        use_eq_var = tk.BooleanVar(value=True)
        use_eq_check = ttk.Checkbutton(eq_frame, text="Apply EQ Settings", variable=use_eq_var)
        use_eq_check.pack(side='left')
        
        use_fir_var = tk.BooleanVar(value=False)
        use_fir_check = ttk.Checkbutton(eq_frame, text="Use Linear-phase FIR (exact)", variable=use_fir_var)
        use_fir_check.pack(side='left', padx=10)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=10)
        
        def create_task():
            output_path = out_var.get()
            if not output_path:
                messagebox.showwarning("Export", "Please select an output file")
                return
                
            # Determine action based on input/output types
            input_type = get_file_type(task.input_path)
            output_type = get_file_type(output_path)
            
            if input_type == 'video' and output_type == 'video':
                action = 'convert_video'
            elif input_type == 'video' and output_type == 'audio':
                action = 'extract_audio'
            elif input_type == 'audio' and output_type == 'audio':
                action = 'convert_audio'
            else:
                action = 'apply_eq'  # Default to EQ processing
            
            # Build options
            options = {
                'format': Path(output_path).suffix.lstrip('.'),
                'sr': int(sr_var.get()),
                'ch': int(ch_var.get()),
                'use_eq': use_eq_var.get(),
                'use_fir': use_fir_var.get()
            }
            
            # Add bitrate options
            if options['format'] in ['mp3']:
                options['mp3_bitrate'] = bitrate_var.get()
            elif options['format'] in ['aac']:
                options['aac_bitrate'] = bitrate_var.get()
            elif options['format'] in ['ogg']:
                options['ogg_bitrate'] = bitrate_var.get()
                
            # Add video-specific options
            if action == 'convert_video':
                options['video_codec'] = vcodec_var.get()
                options['video_bitrate'] = vbitrate_var.get()
                options['audio_codec'] = acodec_var.get()
                options['audio_bitrate'] = bitrate_var.get()
            
            # Create new task
            new_task = Task(
                input_path=task.input_path,
                output_path=output_path,
                action=action,
                options=options,
                id=str(time.time()) + os.path.basename(output_path)
            )
            
            self._tasks.append(new_task)
            self._refresh_task_tree()
            self.log(f'Created export task: {task.input_path} -> {output_path}')
            export_win.destroy()
        
        ttk.Button(btn_frame, text="Export", command=create_task).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Cancel", command=export_win.destroy).pack(side='right')

    def _browse_output_file(self, format_ext: str, out_var: tk.StringVar):
        """Browse for output file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_ext}",
            filetypes=[(f"{format_ext.upper()} files", f"*.{format_ext}")]
        )
        if file_path:
            out_var.set(file_path)

    def start_queue(self):
        # start any pending tasks sequentially or in parallel
        for t in list(self._tasks):
            if t.action in ('apply_eq', 'extract_audio', 'convert_video', 'convert_audio'):
                if t.id not in self._workers:
                    bands_eff = self._effective_bands() if t.options.get('use_eq', True) else []
                    worker = Worker(t, bands_eff, self.ui_queue)
                    self._workers[t.id] = worker
                    worker.start()
                    self.log(f'Started task: {t.input_path} -> {t.output_path}')
        self.status_var.set('Running tasks')

    def stop_all(self):
        # try to terminate ffmpeg procs by killing children workers' processes
        for w in self._workers.values():
            try:
                if getattr(w, '_proc', None):
                    w._proc.kill()
            except Exception:
                pass
        self._workers.clear()
        self.status_var.set('Stopped')

    # ---------------- EQ editor ----------------
    def _build_default_bands(self):
        self.bands = [Band(type='highpass', f=60), Band(type='parametric', f=250, width=1.0, g=-3.0), Band(type='parametric', f=3000, width=1.0, g=2.0), Band(type='lowpass', f=15000)]
        self._render_bands()

    def _render_bands(self):
        for c in self.band_container.winfo_children():
            c.destroy()
        for i, b in enumerate(self.bands):
            fr = ttk.Frame(self.band_container)
            fr.pack(fill='x', pady=2)
            ttk.Label(fr, text=f'#{i+1}').pack(side='left', padx=4)
            tvar = tk.StringVar(value=b.type)
            cb = ttk.Combobox(fr, values=['parametric','highpass','lowpass'], textvariable=tvar, width=10, state='readonly')
            cb.pack(side='left')
            fvar = tk.StringVar(value=str(int(b.f)))
            ttk.Entry(fr, textvariable=fvar, width=8).pack(side='left', padx=6)
            wvar = tk.StringVar(value=str(b.width))
            ttk.Entry(fr, textvariable=wvar, width=6).pack(side='left', padx=6)
            gvar = tk.DoubleVar(value=b.g)
            ttk.Scale(fr, from_=-24, to=24, variable=gvar, orient='horizontal', length=160).pack(side='left', padx=6)
            mute_btn = ttk.Button(fr, text='Mute' if not b.muted else 'Muted', width=6, command=lambda idx=i: self._toggle_mute(idx))
            mute_btn.pack(side='right', padx=4)
            solo_btn = ttk.Button(fr, text='Solo' if not b.solo else 'Soloed', width=6, command=lambda idx=i: self._toggle_solo(idx))
            solo_btn.pack(side='right')
            inv_btn = ttk.Button(fr, text='Invert' if not b.invert else 'Inverted', width=8, command=lambda idx=i: self._toggle_invert(idx))
            inv_btn.pack(side='right', padx=4)
            rm = ttk.Button(fr, text='Remove', command=lambda idx=i: self._remove_band(idx))
            rm.pack(side='right', padx=4)
            cb.bind('<<ComboboxSelected>>', lambda e, idx=i, tv=tvar: self._set_band(idx, 'type', tv.get()))
            fvar.trace_add('write', lambda *a, idx=i, vv=fvar: self._set_band(idx, 'f', vv.get()))
            wvar.trace_add('write', lambda *a, idx=i, vv=wvar: self._set_band(idx, 'width', vv.get()))
            gvar.trace_add('write', lambda *a, idx=i, vv=gvar: self._set_band(idx, 'g', vv.get()))
        self._update_visualiser()

    def add_band(self):
        self.bands.append(Band())
        self._render_bands()

    def _remove_band(self, idx):
        if 0 <= idx < len(self.bands):
            self.bands.pop(idx)
            self._render_bands()

    def _toggle_mute(self, idx):
        self.bands[idx].muted = not self.bands[idx].muted
        self._render_bands()

    def _toggle_solo(self, idx):
        self.bands[idx].solo = not self.bands[idx].solo
        self._render_bands()

    def _toggle_invert(self, idx):
        self.bands[idx].invert = not self.bands[idx].invert
        self._render_bands()

    def _set_band(self, idx, field, value):
        try:
            if field == 'type':
                self.bands[idx].type = value
            elif field == 'f':
                self.bands[idx].f = float(value)
            elif field == 'width':
                self.bands[idx].width = float(value)
            elif field == 'g':
                self.bands[idx].g = float(value)
        except Exception:
            pass
        self._update_visualiser()

    def _effective_bands(self) -> List[Band]:
        if any(b.solo for b in self.bands):
            return [b.copy() for b in self.bands if b.solo]
        return [b.copy() for b in self.bands if not b.muted]

    # ---------------- Preview and A/B features ----------------
    def preview_choice_threaded(self):
        use_fir = messagebox.askyesno('Preview mode', 'Use linear-phase FIR for preview? (may be slow)')
        threading.Thread(target=lambda: self._preview(use_fir), daemon=True).start()

    def _preview(self, use_fir: bool = False):
        try:
            self._set_all_buttons_state('disabled')
            src = filedialog.askopenfilename(title='Select source for preview')
            if not src:
                return
            tmp_in = os.path.join(tempfile.gettempdir(), f'umc_preview_in_{int(time.time())}.wav')
            cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', src, '-t', str(PREVIEW_DURATION), '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', tmp_in]
            self.log('Rendering source...')
            rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if rc != 0:
                self.log('ffmpeg failed')
                return
            if use_fir:
                if not NP_AVAILABLE:
                    self.log('numpy required for FIR preview')
                    return
                taps = max(64, 2048)
                self.log('Designing FIR (preview)...')
                fir = design_linear_phase_fir(self._effective_bands(), 44100, taps)
                tmp_out = os.path.join(tempfile.gettempdir(), f'umc_preview_out_{int(time.time())}.wav')
                overlap_add_convolve_wav(tmp_in, fir, tmp_out, block_size=65536, ui_queue=self.ui_queue, task_id='preview')
                self._play_file(tmp_out)
            else:
                filters = build_ffmpeg_filter(self._effective_bands())
                tmp_out = os.path.join(tempfile.gettempdir(), f'umc_preview_out_{int(time.time())}.wav')
                cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_in]
                if filters:
                    cmd += ['-af', filters]
                cmd += ['-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', tmp_out]
                rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if rc == 0:
                    self._play_file(tmp_out)
                else:
                    self.log('ffmpeg preview failed')
        except Exception as e:
            self.log(f'Preview error: {e}')
        finally:
            self._set_all_buttons_state('normal')

    def _play_file(self, path: str):
        try:
            if not SIMPLEAUDIO_AVAILABLE:
                self.log('simpleaudio not installed')
                return
            if getattr(self, '_play_obj', None):
                try:
                    self._play_obj.stop()
                except Exception:
                    pass
            wobj = sa.WaveObject.from_wave_file(path)
            self._play_obj = wobj.play()
        except Exception as e:
            self.log(f'Play error: {e}')

    def ab_crossfade_threaded(self):
        threading.Thread(target=self._ab_crossfade, daemon=True).start()

    def _ab_crossfade(self):
        try:
            self._set_all_buttons_state('disabled')
            if self.ab_a is None or self.ab_b is None:
                messagebox.showinfo('A/B', 'Save both A and B first')
                return
            src = filedialog.askopenfilename(title='Select source for A/B crossfade')
            if not src:
                return
            # render base
            tmp_in = os.path.join(tempfile.gettempdir(), f'umc_ab_in_{int(time.time())}.wav')
            cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', src, '-t', str(PREVIEW_DURATION), '-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', tmp_in]
            rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if rc != 0:
                self.log('ffmpeg failed to render base')
                return
            # render A and B
            tmp_a = os.path.join(tempfile.gettempdir(), f'umc_ab_a_{int(time.time())}.wav')
            tmp_b = os.path.join(tempfile.gettempdir(), f'umc_ab_b_{int(time.time())}.wav')
            filters_a = build_ffmpeg_filter(self.ab_a)
            filters_b = build_ffmpeg_filter(self.ab_b)
            cmd_a = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_in]
            if filters_a: cmd_a += ['-af', filters_a]
            cmd_a += ['-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', tmp_a]
            cmd_b = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-i', tmp_in]
            if filters_b: cmd_b += ['-af', filters_b]
            cmd_b += ['-ar', '44100', '-ac', '2', '-c:a', 'pcm_s16le', tmp_b]
            subprocess.call(cmd_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.call(cmd_b, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # mix crossfade
            with wave.open(tmp_a, 'rb') as wa, wave.open(tmp_b, 'rb') as wb:
                nch = wa.getnchannels(); sr = wa.getframerate()
                a_raw = wa.readframes(wa.getnframes())
                b_raw = wb.readframes(wb.getnframes())
            if NP_AVAILABLE:
                a_arr = np.frombuffer(a_raw, dtype=np.int16).astype(np.float32).reshape(-1, nch)
                b_arr = np.frombuffer(b_raw, dtype=np.int16).astype(np.float32).reshape(-1, nch)
                L = max(a_arr.shape[0], b_arr.shape[0])
                def pad(a):
                    if a.shape[0] < L:
                        return np.vstack([a, np.zeros((L - a.shape[0], a.shape[1]))])
                    return a[:L]
                a_arr = pad(a_arr); b_arr = pad(b_arr)
                t = np.linspace(0,1,L)[:,None]
                out = a_arr * (1 - t) + b_arr * t
                maxv = np.max(np.abs(out));
                if maxv < 1e-9: maxv = 1.0
                out_int = (out * (32767.0 / maxv)).astype(np.int16)
            else:
                # Fallback when numpy is not available - just play one of the files
                self._play_file(tmp_a)
                return
            tmp_out = os.path.join(tempfile.gettempdir(), f'umc_ab_xfade_{int(time.time())}.wav')
            with wave.open(tmp_out, 'wb') as wf:
                wf.setnchannels(nch); wf.setsampwidth(2); wf.setframerate(sr)
                wf.writeframes(out_int.tobytes())
            self._play_file(tmp_out)
        except Exception as e:
            self.log(f'AB crossfade error: {e}')
        finally:
            self._set_all_buttons_state('normal')

    # ---------------- FIR export ----------------
    def export_fir_coeffs_dialog(self):
        if not NP_AVAILABLE:
            messagebox.showinfo('Export FIR', 'numpy required')
            return
        csv_path = filedialog.asksaveasfilename(defaultextension='.csv', title='Save FIR coefficients (CSV)')
        if not csv_path:
            return
        n_taps = 2048
        try:
            n_taps = int(simpledialog := None or 2048)
        except Exception:
            pass
        coeffs = design_linear_phase_fir(self._effective_bands(), 44100, n_taps)
        with open(csv_path, 'w', encoding='utf-8') as fh:
            fh.write('index,coef\n')
            for i, c in enumerate(coeffs):
                fh.write(f'{i},{float(c):.12e}\n')
        base = os.path.splitext(csv_path)[0]
        raw_path = base + '.f32'
        wav_ir = base + '_IR.wav'
        with open(raw_path, 'wb') as fh:
            fh.write(coeffs.astype(np.float32).tobytes())
        cmd = [which_exe('ffmpeg') or 'ffmpeg', '-y', '-f', 'f32le', '-ar', '44100', '-ac', '1', '-i', raw_path, wav_ir]
        rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if rc == 0:
            self.log(f'IR WAV generated: {wav_ir}')
        else:
            self.log('IR WAV generation failed (but .f32/.csv are available)')

    # ---------------- Presets ----------------
    def _load_presets(self):
        if PRESETS_FILE.exists():
            try:
                with open(PRESETS_FILE, 'r', encoding='utf-8') as fh:
                    self._preset_store = json.load(fh)
            except Exception:
                self._preset_store = {'presets': []}
        else:
            self._preset_store = {'presets': []}
            try:
                with open(PRESETS_FILE, 'w', encoding='utf-8') as fh:
                    json.dump(self._preset_store, fh, indent=2)
            except Exception:
                pass

    def save_preset(self):
        name = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('Preset','*.json')])
        if not name:
            return
        payload = {'bands':[asdict(b) for b in self.bands]}
        with open(name, 'w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2)
        self._preset_store.setdefault('presets', []).append({'name': os.path.basename(name), 'file': name})
        with open(PRESETS_FILE, 'w', encoding='utf-8') as fh:
            json.dump(self._preset_store, fh, indent=2)
        self.log(f'Preset saved: {name}')

    def load_preset(self):
        f = filedialog.askopenfilename(filetypes=[('Preset','*.json')])
        if not f:
            return
        with open(f, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
        self.bands = [Band(**b) for b in payload.get('bands', [])]
        self._render_bands()
        self.log(f'Loaded preset: {f}')

    # ---------------- A/B ----------------
    def save_ab_a(self):
        self.ab_a = [b.copy() for b in self.bands]
        self.log('Saved A')

    def save_ab_b(self):
        self.ab_b = [b.copy() for b in self.bands]
        self.log('Saved B')

    def toggle_ab(self):
        if self.ab_a is None or self.ab_b is None:
            messagebox.showinfo('A/B', 'Save both A and B first')
            return
        if getattr(self, '_ab_state', None) == 'A':
            self.bands = [b.copy() for b in self.ab_b]
            self._ab_state = 'B'
            self.log('Switched to B')
        else:
            self.bands = [b.copy() for b in self.ab_a]
            self._ab_state = 'A'
            self.log('Switched to A')
        self._render_bands()

    # ---------------- helpers & UI loop ----------------
    def _start_ui_loop(self):
        self.root.after(200, self._ui_loop)

    def _ui_loop(self):
        try:
            while True:
                typ, payload = self.ui_queue.get_nowait()
                if typ == 'log':
                    self.log(payload)
                elif typ == 'cmd':
                    self.log('CMD: ' + payload)
                elif typ == 'progress':
                    task_id, pct = payload
                    self.global_progress['value'] = pct
                    if self.task_tree.exists(task_id):
                        self.task_tree.set(task_id, 'progress', f'{pct:.1f}%')
                elif typ == 'error':
                    self.log('ERROR: ' + payload)
                    self.root.after(0, lambda: messagebox.showerror(APP_TITLE, payload))
                elif typ == 'done':
                    self.log(f'Task {payload} done')
        except queue.Empty:
            pass
        # redraw visualiser periodically
        self._update_visualiser()
        self.root.after(200, self._ui_loop)

    def _update_visualiser(self):
        if not (MATPLOTLIB_AVAILABLE and NP_AVAILABLE and hasattr(self, 'ax')):
            return
        try:
            fs = 4100.0
            if NP_AVAILABLE:
                freqs = np.logspace(math.log10(20.0), math.log10(20000.0), num=2048)
                H = compute_total_response(self._effective_bands(), freqs, fs)
                mag = 20 * np.log10(np.maximum(np.abs(H), 1e-12))
                self.ax.clear(); self.ax.set_xscale('log'); self.ax.set_xlim(20,20000); self.ax.set_ylim(-36,36)
                self.ax.grid(True, which='both', ls='--', alpha=0.3)
                self.ax.plot(freqs, mag, linewidth=2)
                for b in self._effective_bands():
                    if b.type == 'parametric':
                        Hb = peaking_eq_response(b, freqs, fs)
                    elif b.type == 'lowpass':
                        Hb = lowpass_response(b.f, freqs, fs)
                    elif b.type == 'highpass':
                        Hb = highpass_response(b.f, freqs, fs)
                    else:
                        Hb = np.ones_like(freqs)
                    mb = 20 * np.log10(np.maximum(np.abs(Hb), 1e-12))
                    self.ax.plot(freqs, mb, alpha=0.35)
                self.canvas_fig.draw()
        except Exception:
            pass

    def _set_all_buttons_state(self, state: str):
        def set_state(w):
            try:
                if isinstance(w, ttk.Button):
                    w.config(state=state)
            except Exception:
                pass
            for ch in w.winfo_children():
                set_state(ch)
        set_state(self.root)

    def _on_drop(self, event):
        data = event.data
        parts = []
        cur = ''
        in_brace = False
        for ch in data:
            if ch == '{': in_brace = True; cur = ''
            elif ch == '}': in_brace = False; parts.append(cur); cur = ''
            elif in_brace: cur += ch
            elif ch == ' ' and not in_brace: continue
        if not parts and data:
            parts = data.split()
        for p in parts:
            if os.path.isdir(p):
                self.add_folder_path(p)
            else:
                self._add_file_to_queue(p)

    def add_folder_path(self, folder: str):
        for root, dirs, files in os.walk(folder):
            for f in files:
                if Path(f).suffix.lower().lstrip('.') in ALL_FORMATS:
                    self._add_file_to_queue(os.path.join(root, f))

    def log(self, text: str):
        ts = time.strftime('%H:%M:%S')
        self.log_text.insert('end', f'[{ts}] {text}\n')
        self.log_text.see('end')
        lines = int(self.log_text.index('end-1c').split('.')[0])
        if lines > LOG_MAX_LINES:
            self.log_text.delete('1.0', f'{lines-LOG_MAX_LINES}.0')

    # ---------------- Export visual ----------------
    def export_visual_png(self):
        if not (MATPLOTLIB_AVAILABLE and NP_AVAILABLE and hasattr(self, 'figure')):
            messagebox.showinfo('Export', 'matplotlib not available')
            return
        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG files', '*.png')])
        if path:
            try:
                self.figure.savefig(path, dpi=300, bbox_inches='tight')
                self.log(f'Visual exported to: {path}')
            except Exception as e:
                self.log(f'Export failed: {e}')

    def export_visual_csv(self):
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not path:
            return
        try:
            fs = 44100.0
            if NP_AVAILABLE:
                freqs = np.logspace(math.log10(20.0), math.log10(20000.0), num=2048)
                H = compute_total_response(self._effective_bands(), freqs, fs)
                mag = 20 * np.log10(np.maximum(np.abs(H), 1e-12))
                with open(path, 'w', encoding='utf-8') as fh:
                    fh.write('frequency, magnitude\n')
                    for f, m in zip(freqs, mag):
                        fh.write(f'{f:.2f},{m:.2f}\n')
                self.log(f'CSV exported to: {path}')
            else:
                self.log('CSV export requires numpy')
        except Exception as e:
            self.log(f'CSV export failed: {e}')

# ---------------- Entry point ----------------

def main():
    if DND_AVAILABLE and 'TkinterDnD' in globals():
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    if which_exe('ffmpeg') is None:
        print('Warning: ffmpeg not found in PATH. Install to enable processing.')
    app = UnifiedApp(root)
    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.mainloop()

if __name__ == '__main__':
    main()
