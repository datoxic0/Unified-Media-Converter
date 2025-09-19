Usage Guide
===========

This guide explains how to use Unified Media Converter v7 for various audio and video conversion tasks.

Getting Started
---------------

Launching the Application
^^^^^^^^^^^^^^^^^^^^^^^^

To start Unified Media Converter v7:

.. code-block:: bash

   python unified_media_converter.py

Or if installed as a package:

.. code-block:: bash

   unified-media-converter

Upon launching, you'll see the main interface with three main sections:

1. **Task Queue Panel** (Left): Lists all queued conversion tasks
2. **EQ Editor Panel** (Middle): Parametric EQ editor with visualization
3. **Preview & Logs Panel** (Right): Real-time preview, visualization, and logs

Adding Files
^^^^^^^^^^^^

There are several ways to add files to the conversion queue:

1. **Add Files Button**: Click the "Add Files" button in the toolbar to select individual files
2. **Add Folder Button**: Click the "Add Folder" button to add all supported files from a directory
3. **Drag and Drop**: Drag files or folders directly onto the application window
4. **Keyboard Shortcut**: Press ``Ctrl+O`` to open the file selection dialog

Supported File Formats
^^^^^^^^^^^^^^^^^^^^^

Video Formats:
- MP4 (.mp4)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)

Audio Formats:
- MP3 (.mp3)
- AAC (.aac)
- FLAC (.flac)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)
- WMA (.wma)

Basic Conversion Workflow
------------------------

1. **Add Source Files**: Use any of the methods described above to add files to the queue
2. **Configure EQ Settings**: Adjust the parametric EQ bands as needed (optional)
3. **Set Output Options**: Double-click a queued task to configure output format and quality
4. **Start Conversion**: Click the "Start Queue" button to begin processing
5. **Monitor Progress**: Watch the progress bar and logs for status updates

Advanced EQ Editor
-----------------

The parametric EQ editor allows precise control over audio frequencies.

Adding EQ Bands
^^^^^^^^^^^^^^^

1. Click the "Add Band" button in the EQ editor panel
2. Select the band type (parametric, highpass, or lowpass)
3. Adjust frequency, width, and gain parameters
4. Use the mute, solo, and invert buttons for advanced control

Band Types
^^^^^^^^^^

1. **Parametric**: Full control over frequency, width (Q or octave), and gain
2. **Highpass**: Filters frequencies below the cutoff frequency
3. **Lowpass**: Filters frequencies above the cutoff frequency

Band Controls
^^^^^^^^^^^^^

- **Frequency (f)**: Center frequency for parametric bands, cutoff frequency for filters
- **Width Type**: Q-factor or octave width for parametric bands
- **Width**: Bandwidth value (Q or octave)
- **Gain (g)**: Boost or cut amount in dB for parametric bands
- **Mute**: Temporarily disable a band
- **Solo**: Listen to only this band
- **Invert**: Flip the phase/polarity of a band

A/B Comparison
^^^^^^^^^^^^^^

1. **Save A**: Click "Save A" to store current EQ settings
2. **Save B**: Modify EQ settings and click "Save B"
3. **Toggle A/B**: Switch between A and B settings instantly
4. **A/B Crossfade**: Seamlessly crossfade between A and B settings

Preview Features
----------------

Preview allows you to audition EQ settings before applying them to full files.

Render & Play Preview
^^^^^^^^^^^^^^^^^^^^

1. Click "Render & Play Preview" in the preview panel
2. Select a source file for preview
3. Choose between FFmpeg filter chain (fast) or linear-phase FIR (exact) processing
4. Listen to the preview and adjust EQ settings as needed

Export Options
--------------

When you double-click a queued task, you'll see the export options dialog.

Output Format Selection
^^^^^^^^^^^^^^^^^^^^^^

Choose from various output formats based on the source file type:

Video Sources:
- Video formats: MP4, AVI, MKV, MOV
- Audio formats: MP3, AAC, FLAC, WAV, M4A

Audio Sources:
- Audio formats: MP3, AAC, FLAC, WAV, M4A, OGG

Quality Options
^^^^^^^^^^^^^^^

Adjust quality settings for optimal output:

1. **Sample Rate**: Choose from 8000, 11025, 12000, 16000, 22050, 24000, 32000, 44100, 48000 Hz
2. **Channels**: Mono (1) or Stereo (2)
3. **Bitrate**: Select appropriate bitrate for the chosen format (64k, 128k, 192k, 256k, 320k)

EQ Processing Options
^^^^^^^^^^^^^^^^^^^^^

1. **Apply EQ Settings**: Enable/disable EQ processing
2. **Use Linear-phase FIR**: Choose between FFmpeg filter chain (fast) or exact linear-phase FIR (precise)

Video-Specific Options
^^^^^^^^^^^^^^^^^^^^^^

For video-to-video conversions:

1. **Video Codec**: libx264, libx265, vp9, or copy (passthrough)
2. **Video Bitrate**: 500k, 1000k, 2000k, or 4000k
3. **Audio Codec**: aac, mp3, flac, or copy (passthrough)
4. **Audio Bitrate**: 64k, 128k, 192k, 256k, or 320k

Batch Processing
----------------

Unified Media Converter v7 supports batch processing of multiple files.

Queue Management
^^^^^^^^^^^^^^^^

1. **Add Multiple Files**: Select multiple files using Shift/Ctrl in the file dialog
2. **Add Folder**: Add all supported files from a directory recursively
3. **Queue Status**: Monitor progress of individual tasks in the task queue
4. **Start Queue**: Process all queued tasks sequentially or in parallel

Progress Tracking
^^^^^^^^^^^^^^^^^

1. **Global Progress Bar**: Shows overall conversion progress
2. **Per-Task Progress**: Individual task progress indicators
3. **Detailed Logs**: Real-time logging of conversion status and errors

Advanced Features
----------------

FIR Coefficient Export
^^^^^^^^^^^^^^^^^^^^^^

Export FIR coefficients for use with external tools:

1. Click "Save FIR Coeffs" in the toolbar
2. Choose export format:
   - CSV: Human-readable coefficient values
   - .f32: Raw 32-bit float binary data
   - IR WAV: Impulse response WAV file for FFmpeg afir filter

Visualization
^^^^^^^^^^^^^

1. **Frequency Response Graph**: Real-time visualization of EQ settings
2. **Export Visual (PNG)**: Save graph as high-resolution PNG image
3. **Export Visual (CSV)**: Export frequency response data as CSV

Presets
^^^^^^^

1. **Save Preset**: Save current EQ settings as a preset
2. **Load Preset**: Load previously saved EQ settings
3. **Per-Band Presets**: Save/load individual band configurations

Keyboard Shortcuts
^^^^^^^^^^^^^^^^^^

- ``Ctrl+O``: Add files
- ``Ctrl+S``: Save preset
- ``Ctrl+Q``: Quit application
- ``Space``: Play/pause preview
- ``Enter``: Start queue
- ``Esc``: Stop all conversions

Troubleshooting
---------------

Common Issues and Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^

Conversion Fails
""""""""""""""""

**Problem**: Task fails with error message

**Solution**:
1. Check FFmpeg installation and PATH
2. Verify source file integrity
3. Check available disk space
4. Review error logs for specific details

Preview Not Working
"""""""""""

**Problem**: Preview fails to play or produces no audio

**Solution**:
1. Install simpleaudio Python package
2. Check audio device settings
3. Verify source file compatibility
4. Try different preview processing method

EQ Visualization Issues
"""""""""""""""

**Problem**: EQ graph not displaying or updating

**Solution**:
1. Install numpy and matplotlib Python packages
2. Restart the application
3. Check for conflicting Python installations

Performance Issues
""""""""""""""""""

**Problem**: Slow conversion speeds or high CPU usage

**Solution**:
1. Reduce number of simultaneous conversions
2. Lower output quality settings
3. Use hardware acceleration if available
4. Close other resource-intensive applications

Support
-------

For additional help, please:

1. Check the project documentation
2. Search existing GitHub issues
3. Create a new GitHub issue with detailed information
4. Include error logs and system specifications
