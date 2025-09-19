API Reference
=============

This document provides a comprehensive reference for the Unified Media Converter v7 API.

Overview
--------

Unified Media Converter v7 exposes a Python API for programmatic access to its core functionality. The API is organized into several modules:

- **Core Classes**: Main application and worker classes
- **Data Classes**: Task and Band data structures
- **Utilities**: Helper functions for file handling and media information
- **DSP Functions**: Digital signal processing functions for EQ and FIR design
- **FFmpeg Integration**: Wrapper functions for FFmpeg operations

Core Classes
------------

UnifiedApp
^^^^^^^^^^

.. class:: UnifiedApp(root: tk.Tk)

   The main application class that manages the GUI and coordinates all operations.

   .. method:: __init__(self, root: tk.Tk)
      
      Initialize the Unified Media Converter application.
      
      :param root: The root Tkinter window

   .. method:: _build_ui(self)
      
      Build the main user interface.
      
      :returns: None

   .. method:: add_files(self)
      
      Add files to the conversion queue via file dialog.
      
      :returns: None

   .. method:: add_folder(self)
      
      Add all files from a folder to the conversion queue.
      
      :returns: None

   .. method:: _add_file_to_queue(self, path: str)
      
      Add a single file to the conversion queue.
      
      :param path: Path to the file to add
      :returns: None

   .. method:: _refresh_task_tree(self)
      
      Refresh the task tree view in the GUI.
      
      :returns: None

   .. method:: _on_task_double(self, event)
      
      Handle double-click events on task tree items.
      
      :param event: The double-click event
      :returns: None

   .. method:: _create_export_dialog(self, task: Task)
      
      Create an export dialog for a queued task.
      
      :param task: The task to create an export dialog for
      :returns: None

   .. method:: _browse_output_file(self, format_ext: str, out_var: tk.StringVar)
      
      Browse for an output file.
      
      :param format_ext: The file extension for the output file
      :param out_var: StringVar to store the selected file path
      :returns: None

   .. method:: start_queue(self)
      
      Start processing all queued tasks.
      
      :returns: None

   .. method:: stop_all(self)
      
      Stop all currently running tasks.
      
      :returns: None

   .. method:: _build_default_bands(self)
      
      Build the default EQ bands.
      
      :returns: None

   .. method:: _render_bands(self)
      
      Render the EQ bands in the GUI.
      
      :returns: None

   .. method:: add_band(self)
      
      Add a new EQ band.
      
      :returns: None

   .. method:: _remove_band(self, idx)
      
      Remove an EQ band by index.
      
      :param idx: Index of the band to remove
      :returns: None

   .. method:: _toggle_mute(self, idx)
      
      Toggle mute state of an EQ band.
      
      :param idx: Index of the band to toggle
      :returns: None

   .. method:: _toggle_solo(self, idx)
      
      Toggle solo state of an EQ band.
      
      :param idx: Index of the band to toggle
      :returns: None

   .. method:: _toggle_invert(self, idx)
      
      Toggle invert state of an EQ band.
      
      :param idx: Index of the band to toggle
      :returns: None

   .. method:: _set_band(self, idx, field, value)
      
      Set a property of an EQ band.
      
      :param idx: Index of the band to modify
      :param field: Property to set ('type', 'f', 'width', 'g')
      :param value: Value to set
      :returns: None

   .. method:: _effective_bands(self) -> List[Band]
      
      Get the effective list of EQ bands (considering solo/mute states).
      
      :returns: List of effective EQ bands

   .. method:: preview_choice_threaded(self)
      
      Start preview in a separate thread.
      
      :returns: None

   .. method:: _preview(self, use_fir: bool = False)
      
      Render and play a preview of the current EQ settings.
      
      :param use_fir: Whether to use linear-phase FIR for preview
      :returns: None

   .. method:: _play_file(self, path: str)
      
      Play an audio file.
      
      :param path: Path to the audio file to play
      :returns: None

   .. method:: ab_crossfade_threaded(self)
      
      Start A/B crossfade in a separate thread.
      
      :returns: None

   .. method:: _ab_crossfade(self)
      
      Perform A/B crossfade between saved EQ settings.
      
      :returns: None

   .. method:: export_fir_coeffs_dialog(self)
      
      Export FIR coefficients via dialog.
      
      :returns: None

   .. method:: _load_presets(self)
      
      Load saved presets from file.
      
      :returns: None

   .. method:: save_preset(self)
      
      Save current EQ settings as a preset.
      
      :returns: None

   .. method:: load_preset(self)
      
      Load EQ settings from a preset file.
      
      :returns: None

   .. method:: save_ab_a(self)
      
      Save current EQ settings as A.
      
      :returns: None

   .. method:: save_ab_b(self)
      
      Save current EQ settings as B.
      
      :returns: None

   .. method:: toggle_ab(self)
      
      Toggle between A and B EQ settings.
      
      :returns: None

   .. method:: _start_ui_loop(self)
      
      Start the UI update loop.
      
      :returns: None

   .. method:: _ui_loop(self)
      
      Main UI update loop.
      
      :returns: None

   .. method:: _update_visualiser(self)
      
      Update the frequency response visualizer.
      
      :returns: None

   .. method:: _set_all_buttons_state(self, state: str)
      
      Set the state of all buttons in the GUI.
      
      :param state: Button state ('normal', 'disabled', etc.)
      :returns: None

   .. method:: _on_drop(self, event)
      
      Handle drag-and-drop events.
      
      :param event: The drop event
      :returns: None

   .. method:: add_folder_path(self, folder: str)
      
      Add all files from a folder path.
      
      :param folder: Path to the folder to add
      :returns: None

   .. method:: log(self, text: str)
      
      Log a message to the GUI log.
      
      :param text: Message to log
      :returns: None

   .. method:: export_visual_png(self)
      
      Export the frequency response visualization as PNG.
      
      :returns: None

   .. method:: export_visual_csv(self)
      
      Export the frequency response data as CSV.
      
      :returns: None

Worker
^^^^^^

.. class:: Worker(task: Task, bands: List[Band], ui_queue: queue.Queue)

   Worker thread class that handles individual conversion tasks.

   .. method:: __init__(self, task: Task, bands: List[Band], ui_queue: queue.Queue)
      
      Initialize the worker thread.
      
      :param task: The task to process
      :param bands: List of EQ bands to apply
      :param ui_queue: Queue for UI updates

   .. method:: run(self)
      
      Main worker thread execution method.
      
      :returns: None

   .. method:: _run_cmd_with_progress(self, cmd: List[str], input_path: Optional[str] = None)
      
      Run an FFmpeg command with progress tracking.
      
      :param cmd: Command to run
      :param input_path: Path to input file (for duration calculation)
      :returns: None

   .. method:: _apply_eq(self)
      
      Apply EQ settings to a file.
      
      :returns: None

   .. method:: _extract_audio(self)
      
      Extract audio from a video file.
      
      :returns: None

   .. method:: _convert_video(self)
      
      Convert a video file to another format.
      
      :returns: None

   .. method:: _convert_audio(self)
      
      Convert an audio file to another format.
      
      :returns: None

Data Classes
------------

Band
^^^^

.. class:: Band(type: str = 'parametric', f: float = 1000.0, width_type: str = 'q', width: float = 1.0, g: float = 0.0, muted: bool = False, solo: bool = False, invert: bool = False)

   Data class representing an EQ band.

   .. attribute:: type
      
      Type of the band ('parametric', 'highpass', 'lowpass')

   .. attribute:: f
      
      Frequency in Hz

   .. attribute:: width_type
      
      Width type ('q' for Q-factor, 'oct' for octave)

   .. attribute:: width
      
      Width value (Q-factor or octave)

   .. attribute:: g
      
      Gain in dB

   .. attribute:: muted
      
      Whether the band is muted

   .. attribute:: solo
      
      Whether the band is soloed

   .. attribute:: invert
      
      Whether the band is inverted (phase flipped)

   .. method:: copy(self) -> 'Band'
      
      Create a copy of the band.
      
      :returns: A copy of the band

Task
^^^^

.. class:: Task(input_path: str, output_path: str, action: str, options: Dict[str, Any], id: Optional[str] = None)

   Data class representing a conversion task.

   .. attribute:: input_path
      
      Path to the input file

   .. attribute:: output_path
      
      Path to the output file

   .. attribute:: action
      
      Action to perform ('apply_eq', 'extract_audio', 'convert_video', 'convert_audio', 'noop')

   .. attribute:: options
      
      Dictionary of options for the task

   .. attribute:: id
      
      Unique identifier for the task

Utilities
---------

which_exe
^^^^^^^^^

.. function:: which_exe(name: str) -> Optional[str]

   Find the path to an executable in the system PATH.
   
   :param name: Name of the executable to find
   :returns: Path to the executable, or None if not found

ffprobe_duration
^^^^^^^^^^^^^^^^

.. function:: ffprobe_duration(path: str) -> float

   Get the duration of a media file using ffprobe.
   
   :param path: Path to the media file
   :returns: Duration in seconds

get_file_type
^^^^^^^^^^^^^

.. function:: get_file_type(path: str) -> str

   Determine if a file is audio or video based on its extension.
   
   :param path: Path to the file
   :returns: 'audio', 'video', or 'unknown'

get_media_info
^^^^^^^^^^^^^^

.. function:: get_media_info(path: str) -> Dict[str, Any]

   Get detailed media information using ffprobe.
   
   :param path: Path to the media file
   :returns: Dictionary of media information

parse_ffmpeg_time
^^^^^^^^^^^^^^^^^

.. function:: parse_ffmpeg_time(line: str) -> Optional[float]

   Parse time information from FFmpeg output.
   
   :param line: Line of FFmpeg output
   :returns: Time in seconds, or None if not found

build_ffmpeg_filter
^^^^^^^^^^^^^^^^^^^

.. function:: build_ffmpeg_filter(bands: List[Band]) -> str

   Build an FFmpeg filter string from EQ bands.
   
   :param bands: List of EQ bands
   :returns: FFmpeg filter string

DSP Functions
-------------

peaking_eq_response
^^^^^^^^^^^^^^^^^^^

.. function:: peaking_eq_response(band: Band, freqs: np.ndarray, fs: float) -> np.ndarray

   Calculate the frequency response of a peaking EQ band.
   
   :param band: The EQ band
   :param freqs: Array of frequencies to calculate response for
   :param fs: Sample rate
   :returns: Complex frequency response

lowpass_response
^^^^^^^^^^^^^^^^

.. function:: lowpass_response(fc: float, freqs: np.ndarray, fs: float) -> np.ndarray

   Calculate the frequency response of a lowpass filter.
   
   :param fc: Cutoff frequency
   :param freqs: Array of frequencies to calculate response for
   :param fs: Sample rate
   :returns: Complex frequency response

highpass_response
^^^^^^^^^^^^^^^^^

.. function:: highpass_response(fc: float, freqs: np.ndarray, fs: float) -> np.ndarray

   Calculate the frequency response of a highpass filter.
   
   :param fc: Cutoff frequency
   :param freqs: Array of frequencies to calculate response for
   :param fs: Sample rate
   :returns: Complex frequency response

compute_total_response
^^^^^^^^^^^^^^^^^^^^^^

.. function:: compute_total_response(bands: List[Band], freqs: np.ndarray, fs: float) -> np.ndarray

   Calculate the total frequency response of multiple EQ bands.
   
   :param bands: List of EQ bands
   :param freqs: Array of frequencies to calculate response for
   :param fs: Sample rate
   :returns: Complex frequency response

design_linear_phase_fir
^^^^^^^^^^^^^^^^^^^^^^^

.. function:: design_linear_phase_fir(bands: List[Band], fs: int, n_taps: int = 2048) -> np.ndarray

   Design a linear-phase FIR filter from EQ bands.
   
   :param bands: List of EQ bands
   :param fs: Sample rate
   :param n_taps: Number of filter taps
   :returns: FIR filter coefficients

next_pow2
^^^^^^^^^

.. function:: next_pow2(x: int) -> int

   Find the next power of 2 greater than or equal to x.
   
   :param x: Input value
   :returns: Next power of 2

overlap_add_convolve_wav
^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: overlap_add_convolve_wav(in_wav: str, fir: np.ndarray, out_wav: str, block_size: int = 65536, ui_queue: Optional[queue.Queue] = None, task_id: Optional[str] = None)

   Convolve a WAV file with an FIR filter using overlap-add method.
   
   :param in_wav: Path to input WAV file
   :param fir: FIR filter coefficients
   :param out_wav: Path to output WAV file
   :param block_size: Block size for processing
   :param ui_queue: Queue for UI updates
   :param task_id: Task ID for progress tracking
   :returns: None

FFmpeg Integration
------------------

FFmpeg Wrapper Functions
^^^^^^^^^^^^^^^^^^^^^^^

Unified Media Converter v7 provides wrapper functions for common FFmpeg operations:

.. function:: run_ffmpeg_cmd(cmd: List[str], input_path: Optional[str] = None) -> int

   Run an FFmpeg command and return the exit code.
   
   :param cmd: Command to run
   :param input_path: Path to input file (for duration calculation)
   :returns: FFmpeg exit code

.. function:: extract_audio_from_video(input_path: str, output_path: str, options: Dict[str, Any]) -> int

   Extract audio from a video file.
   
   :param input_path: Path to input video file
   :param output_path: Path to output audio file
   :param options: Dictionary of options
   :returns: FFmpeg exit code

.. function:: convert_video_format(input_path: str, output_path: str, options: Dict[str, Any]) -> int

   Convert a video file to another format.
   
   :param input_path: Path to input video file
   :param output_path: Path to output video file
   :param options: Dictionary of options
   :returns: FFmpeg exit code

.. function:: convert_audio_format(input_path: str, output_path: str, options: Dict[str, Any]) -> int

   Convert an audio file to another format.
   
   :param input_path: Path to input audio file
   :param output_path: Path to output audio file
   :param options: Dictionary of options
   :returns: FFmpeg exit code

Constants
---------

APP_TITLE
^^^^^^^^^

.. data:: APP_TITLE

   Title of the application ('Unified Media Converter v7')

PRESETS_FILE
^^^^^^^^^^^^

.. data:: PRESETS_FILE

   Path to the presets file (``~/.umc_presets.json``)

PREVIEW_DURATION
^^^^^^^^^^^^^^^^

.. data:: PREVIEW_DURATION

   Duration of preview clips in seconds (6)

LOG_MAX_LINES
^^^^^^^^^^^^^

.. data:: LOG_MAX_LINES

   Maximum number of lines in the log (3000)

VIDEO_FORMATS
^^^^^^^^^^^^^

.. data:: VIDEO_FORMATS

   List of supported video formats (['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm'])

AUDIO_FORMATS
^^^^^^^^^^^^^

.. data:: AUDIO_FORMATS

   List of supported audio formats (['mp3', 'aac', 'flac', 'wav', 'm4a', 'ogg', 'wma'])

ALL_FORMATS
^^^^^^^^^^^

.. data:: ALL_FORMATS

   Combined list of all supported formats (VIDEO_FORMATS + AUDIO_FORMATS)

Example Usage
-------------

Basic Usage
^^^^^^^^^^^

Here's a simple example of how to use the Unified Media Converter v7 API:

.. code-block:: python

   from unified_media_converter_v7 import UnifiedApp
   import tkinter as tk
   
   # Create the main application window
   root = tk.Tk()
   
   # Initialize the Unified Media Converter
   app = UnifiedApp(root)
   
   # Start the GUI event loop
   root.mainloop()

Advanced Usage
^^^^^^^^^^^^^^

Here's a more advanced example showing how to programmatically add files and start processing:

.. code-block:: python

   from unified_media_converter_v7 import UnifiedApp, Task
   import tkinter as tk
   import time
   
   # Create the main application window
   root = tk.Tk()
   
   # Initialize the Unified Media Converter
   app = UnifiedApp(root)
   
   # Add a file to the queue programmatically
   task = Task(
       input_path='/path/to/input.mp4',
       output_path='/path/to/output.mp3',
       action='extract_audio',
       options={'format': 'mp3', 'sr': 44100, 'ch': 2, 'mp3_bitrate': '192k'}
   )
   app._tasks.append(task)
   
   # Refresh the task tree to show the new task
   app._refresh_task_tree()
   
   # Start processing the queue
   app.start_queue()
   
   # Start the GUI event loop
   root.mainloop()

Custom EQ Processing
^^^^^^^^^^^^^^^^^^^

Here's an example of how to create custom EQ settings programmatically:

.. code-block:: python

   from unified_media_converter_v7 import UnifiedApp, Band
   import tkinter as tk
   import numpy as np
   
   # Create the main application window
   root = tk.Tk()
   
   # Initialize the Unified Media Converter
   app = UnifiedApp(root)
   
   # Create custom EQ bands
   app.bands = [
       Band(type='highpass', f=60, muted=False, solo=False, invert=False),
       Band(type='parametric', f=250, width_type='q', width=1.0, g=-3.0, muted=False, solo=False, invert=False),
       Band(type='parametric', f=3000, width_type='q', width=1.0, g=2.0, muted=False, solo=False, invert=False),
       Band(type='lowpass', f=15000, muted=False, solo=False, invert=False)
   ]
   
   # Render the bands in the GUI
   app._render_bands()
   
   # Update the visualizer
   app._update_visualiser()
   
   # Start the GUI event loop
   root.mainloop()

FIR Coefficient Export
^^^^^^^^^^^^^^^^^^^^^^

Here's an example of how to export FIR coefficients programmatically:

.. code-block:: python

   from unified_media_converter_v7 import UnifiedApp, design_linear_phase_fir
   import tkinter as tk
   import numpy as np
   
   # Create the main application window
   root = tk.Tk()
   
   # Initialize the Unified Media Converter
   app = UnifiedApp(root)
   
   # Design FIR coefficients from current EQ settings
   coeffs = design_linear_phase_fir(app._effective_bands(), 44100, 2048)
   
   # Export coefficients as CSV
   with open('/path/to/fir_coefficients.csv', 'w') as f:
       f.write('index,coef\n')
       for i, c in enumerate(coeffs):
           f.write(f'{i},{float(c):.12e}\n')
   
   # Export coefficients as raw float32
   with open('/path/to/fir_coefficients.f32', 'wb') as f:
       f.write(coeffs.astype(np.float32).tobytes())
   
   # Start the GUI event loop
   root.mainloop()

Error Handling
--------------

The Unified Media Converter v7 API includes comprehensive error handling:

.. code-block:: python

   from unified_media_converter_v7 import UnifiedApp
   import tkinter as tk
   
   try:
       # Create the main application window
       root = tk.Tk()
       
       # Initialize the Unified Media Converter
       app = UnifiedApp(root)
       
       # Start the GUI event loop
       root.mainloop()
   except Exception as e:
       print(f"Error initializing Unified Media Converter: {e}")
       sys.exit(1)

Best Practices
--------------

When using the Unified Media Converter v7 API, follow these best practices:

1. **Always check for dependencies**: Verify that required libraries (numpy, matplotlib, etc.) are available before using advanced features.

2. **Handle exceptions gracefully**: Wrap API calls in try-except blocks to handle potential errors.

3. **Use appropriate data types**: Ensure that parameters passed to API functions are of the correct type.

4. **Clean up resources**: Properly dispose of temporary files and resources when finished.

5. **Follow threading guidelines**: Use the provided threading utilities for background operations.

6. **Respect UI state**: Use the provided methods to update UI elements rather than manipulating them directly.

7. **Log appropriately**: Use the built-in logging system for debugging and status information.

8. **Validate inputs**: Check that file paths exist and are accessible before processing.

9. **Handle user interruptions**: Gracefully handle user-initiated cancellations.

10. **Test thoroughly**: Test your code with various input formats and edge cases.

Compatibility
-------------

The Unified Media Converter v7 API is compatible with:

- **Python Versions**: 3.8+
- **Operating Systems**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+, Fedora 32+, Debian 11+)
- **FFmpeg Versions**: 4.0+
- **Dependencies**: numpy 1.21+, matplotlib 3.4+, simpleaudio 1.0+, tkinterdnd2 0.3+

Limitations
-----------

The Unified Media Converter v7 API has the following limitations:

1. **Threading constraints**: Some operations must be performed on the main thread due to GUI requirements.

2. **Memory usage**: Large FIR filters and high-resolution visualizations may consume significant memory.

3. **Processing time**: Linear-phase FIR convolution is slower than FFmpeg filter chains.

4. **Platform dependencies**: Some features require specific system libraries or executables.

5. **File format restrictions**: Only certain audio and video formats are supported.

6. **Hardware requirements**: High-quality processing may require significant CPU and memory resources.

7. **Network dependencies**: Some features may require internet access for updates or cloud processing.

Extending the API
-----------------

To extend the Unified Media Converter v7 API:

1. **Add new data classes**: Create new dataclasses for additional functionality.

2. **Implement new worker methods**: Add methods to the Worker class for new processing tasks.

3. **Extend the GUI**: Add new UI elements and callbacks for extended features.

4. **Add new DSP functions**: Implement new signal processing algorithms as needed.

5. **Update documentation**: Document new features in the API reference.

6. **Add unit tests**: Create tests for new functionality.

7. **Maintain compatibility**: Ensure backward compatibility with existing code.

8. **Follow coding standards**: Adhere to the existing code style and conventions.

Support
-------

For support with the Unified Media Converter v7 API:

1. Check the official documentation
2. Search existing GitHub issues
3. Create a new GitHub issue with detailed information
4. Include error logs and system specifications
5. Provide minimal reproduction examples
6. Specify the version of the software you're using
7. Include information about your operating system and Python version
8. List any relevant third-party libraries and their versions
