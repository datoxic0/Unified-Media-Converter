Unified Media Converter v7
========================

A professional, robust, single-file application for audio and video conversion with advanced parametric EQ capabilities.

.. image:: https://img.shields.io/badge/version-7.0.0-blue.svg
   :alt: Version 7.0.0
.. image:: https://img.shields.io/badge/python-3.8+-blue.svg
   :alt: Python 3.8+
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :alt: MIT License
.. image:: https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg
   :alt: Cross-platform

Features
--------

- **Load audio & video files** with drag-and-drop support
- **Batch queue** with start/stop, per-task progress and logs
- **Video -> audio extraction** (MP3/AAC/FLAC/WAV/M4A) with advanced libmp3lame options (CBR/VBR)
- **Video -> video conversion** (MP4/AVI/MKV/MOV) with quality/bitrate options
- **Audio -> audio conversion** (MP3/AAC/FLAC/WAV/M4A/OGG/WMA) with quality/bitrate options
- **Parametric EQ editor** (parametric/highpass/lowpass bands) with per-band mute/solo/invert
- **Preview** with FFmpeg filter or linear-phase FIR (design + overlap-add convolution)
- **Final export options**: FFmpeg filter chain or exact linear-phase FIR convolution
- **Export FIR coefficients** (CSV, .f32 raw, IR WAV for FFmpeg afir)
- **A/B compare** and instant crossfade audition between A and B
- **Real-time FFmpeg progress parsing** and GUI updates
- **Presets** (save/load) and per-band presets
- **UI polish**: drag/drop hotspots, keyboard shortcuts, disabled controls during processing
- **Robust threading**, queue-based UI updates, and defensive error handling

Requirements
------------

Essential
^^^^^^^^^

- **Python 3.8+**
- **ffmpeg and ffprobe** in PATH

Optional but Recommended
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install numpy matplotlib simpleaudio tkinterdnd2

Installation
------------

1. **Install Python Dependencies**

.. code-block:: bash

   # Required
   pip install tkinter

   # Optional but recommended for full functionality
   pip install numpy matplotlib simpleaudio tkinterdnd2

2. **Install FFmpeg**

Windows
~~~~~~~

Using Chocolatey:

.. code-block:: bash

   choco install ffmpeg

Or download from `FFmpeg official site <https://ffmpeg.org/download.html>`_

macOS
~~~~~

Using Homebrew:

.. code-block:: bash

   brew install ffmpeg

Linux (Ubuntu/Debian)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   sudo apt update
   sudo apt install ffmpeg

3. **Download Application**

Save the ``unified_media_converter.py`` file to your preferred location.

Usage
-----

Starting the Application
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   python unified_media_converter.py

Basic Workflow
^^^^^^^^^^^^^^

1. **Add Files**: Click "Add Files" or "Add Folder" to load media files
2. **Configure EQ**: Adjust parametric EQ bands as needed
3. **Set Output Options**: Double-click a queued file to configure conversion settings
4. **Process Files**: Click "Start Queue" to begin conversion

EQ Editor
^^^^^^^^^

- **Add Band**: Click "Add Band" to insert a new parametric EQ band
- **Adjust Parameters**: Use sliders and input fields to set frequency, bandwidth, and gain
- **Band Types**: Switch between parametric, highpass, and lowpass filters
- **Special Controls**:
  - Mute: Temporarily disable a band
  - Solo: Listen to only this band
  - Invert: Flip the phase/polarity of a band

A/B Comparison
^^^^^^^^^^^^^^

1. Configure EQ settings (A)
2. Click "Save A"
3. Modify EQ settings (B)
4. Click "Save B"
5. Use "Toggle A/B" to switch between configurations
6. Use "A/B Crossfade" for seamless comparison

Export Options
^^^^^^^^^^^^^^

When double-clicking a queued file, you can configure:

- **Output Format**: Select from supported audio/video formats
- **Quality Settings**: Sample rate, channels, and bitrate
- **EQ Processing**: Enable/disable EQ application
- **Processing Method**: Choose between FFmpeg filters or linear-phase FIR

Technical Details
-----------------

Supported Formats
^^^^^^^^^^^^^^^^^

Video Input/Output
~~~~~~~~~~~~~~~~~~

- MP4 (.mp4)
- AVI (.avi)
- MKV (.mkv)
- MOV (.mov)
- WMV (.wmv)
- FLV (.flv)
- WebM (.webm)

Audio Input/Output
~~~~~~~~~~~~~~~~~~

- MP3 (.mp3)
- AAC (.aac)
- FLAC (.flac)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)
- WMA (.wma)

DSP Capabilities
^^^^^^^^^^^^^^^^

Parametric EQ Bands
~~~~~~~~~~~~~~~~~~~

Each band supports:

- **Frequency Range**: 1 Hz to Nyquist frequency
- **Bandwidth Control**: Q-factor or octave width
- **Gain Adjustment**: ±24dB boost/cut
- **Filter Types**: Peaking, highpass, lowpass

FIR Processing
~~~~~~~~~~~~~~

- **Linear-phase Design**: Exact frequency response matching
- **Configurable Taps**: Adjustable filter length for quality/performance tradeoff
- **Overlap-add Convolution**: Efficient processing of large files

Performance Optimization
^^^^^^^^^^^^^^^^^^^^^^^

- **Multithreading**: Separate worker threads for each conversion task
- **Memory Management**: Streaming processing for large files
- **Smart Caching**: Reuse computed EQ responses when possible

Troubleshooting
---------------

Common Issues
^^^^^^^^^^^^^

FFmpeg Not Found
~~~~~~~~~~~~~~~~

**Problem**: Warning message about missing FFmpeg
**Solution**: Ensure FFmpeg is installed and in system PATH

No Audio Output
~~~~~~~~~~~~~~~

**Problem**: Converted files have no audio
**Solution**: 
1. Check that audio codecs are properly licensed
2. Verify source file isn't corrupted
3. Try different output format/bitrate combinations

Visualizer Not Working
~~~~~~~~~~~~~~~~~~~~~~

**Problem**: EQ visualization not displayed
**Solution**: Install required packages:

.. code-block:: bash

   pip install numpy matplotlib

Drag & Drop Not Working
~~~~~~~~~~~~~~~~~~~~~~~

**Problem**: Unable to drop files onto application
**Solution**: Install tkinterdnd2:

.. code-block:: bash

   pip install tkinterdnd2

Log Interpretation
^^^^^^^^^^^^^^^^^^

The application provides detailed logging:

- **INFO**: General operation progress
- **CMD**: FFmpeg commands being executed
- **ERROR**: Processing failures with detailed messages
- **WARN**: Non-critical issues that may affect output quality

Compilation to Executable
-------------------------

To compile the application into a standalone executable:

Using PyInstaller
^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install pyinstaller
   pyinstaller --onefile --windowed --icon=app_icon.ico unified_media_converter.py

Using cx_Freeze
^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install cx_Freeze
   cxfreeze unified_media_converter.py --target-dir dist

Logo and Icon Design
--------------------

Logo Design Prompt
^^^^^^^^^^^^^^^^^^

Create a modern, professional logo for "Unified Media Converter" featuring:

1. A stylized representation combining audio waveform and video playback elements
2. Color scheme: Professional blue (#2563EB) and gray tones with accent colors
3. Typography: Clean, modern sans-serif font
4. Symbolism: Unification of audio and video media processing
5. Style: Flat design, scalable for various sizes
6. Additional elements: Subtle technology/processing motifs

Icon Sizes Required
^^^^^^^^^^^^^^^^^^^

For Windows application packaging, the following icon sizes are recommended:

==========  ====================
Size        Purpose
==========  ====================
16x16       Toolbar icons, favicon
24x24       Small toolbar icons
32x32       Taskbar, file explorer
48x48       Medium application icons
64x64       Larger UI elements
128x128     High-DPI displays
256x256     Modern high-resolution displays
==========  ====================

Inno Setup Script
^^^^^^^^^^^^^^^^^

For creating a Windows installer, use the following Inno Setup script template:

.. code-block:: ini

   [Setup]
   AppName=Unified Media Converter
   AppVersion=7.0
   DefaultDirName={pf}\UnifiedMediaConverter
   DefaultGroupName=Unified Media Converter
   Compression=lzma
   SolidCompression=yes
   OutputDir=.
   OutputBaseFilename=unified_media_converter_setup
   SetupIconFile=app_icon.ico

   [Files]
   Source: "dist\unified_media_converter.exe"; DestDir: "{app}"; Flags: ignoreversion
   Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

   [Icons]
   Name: "{group}\Unified Media Converter"; Filename: "{app}\unified_media_converter.exe"; IconFilename: "{app}\unified_media_converter.exe"
   Name: "{group}\Uninstall Unified Media Converter"; Filename: "{uninstallexe}"
   Name: "{autodesktop}\Unified Media Converter"; Filename: "{app}\unified_media_converter.exe"; IconFilename: "{app}\unified_media_converter.exe"

   [Run]
   Filename: "{app}\unified_media_converter.exe"; Description: "{cm:LaunchProgram,Unified Media Converter}"; Flags: nowait postinstall skipifsilent

Contributing
------------

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
---------------

- FFmpeg project for powerful multimedia processing capabilities
- NumPy and Matplotlib for scientific computing and visualization
- Tkinter for GUI framework
- Simpleaudio for cross-platform audio playback
- TkinterDnD for drag-and-drop functionality

Changelog
---------

Version 7.0
^^^^^^^^^^^

- Added comprehensive video-to-video conversion capabilities
- Enhanced audio-to-audio conversion with more format support
- Improved parametric EQ editor with visualization
- Added FIR coefficient export functionality
- Implemented batch processing queue with progress tracking
- Added A/B comparison and crossfade audition
- Improved UI with drag-and-drop support
- Added preset management system

Version 6.0
^^^^^^^^^^^

- Initial release with basic audio conversion and EQ capabilities

Support
-------

For support, feature requests, or bug reports, please open an issue on the project repository.
