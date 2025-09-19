Unified Media Converter v7 Documentation
======================================

Welcome to the documentation for Unified Media Converter v7, a professional, robust, single-file application for audio and video conversion with advanced parametric EQ capabilities.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   usage
   features
   api
   contributing
   changelog

Introduction
------------

Unified Media Converter v7 is an enhanced unified toolkit that combines and expands upon previous versions to provide comprehensive audio and video conversion capabilities. The application features:

- Load audio & video files with drag-and-drop support
- Batch queue with start/stop, per-task progress and logs
- Video -> audio extraction with advanced libmp3lame options (CBR/VBR)
- Video -> video conversion with quality/bitrate options
- Audio -> audio conversion with quality/bitrate options
- Parametric EQ editor with per-band mute/solo/invert
- Preview with FFmpeg filter or linear-phase FIR convolution
- Final export options: FFmpeg filter chain or exact linear-phase FIR convolution
- Export FIR coefficients (CSV, .f32 raw, IR WAV for FFmpeg afir)
- A/B compare and instant crossfade audition between A and B
- Real-time FFmpeg progress parsing and GUI updates
- Presets (save/load) and per-band presets
- UI polish: drag/drop hotspots, keyboard shortcuts, disabled controls during processing
- Robust threading, queue-based UI updates, and defensive error handling

Requirements
------------

- Python 3.8+
- ffmpeg and ffprobe in PATH
- Optional but recommended: pip install numpy matplotlib simpleaudio tkinterdnd2

Installation
------------

See :doc:`installation` for detailed installation instructions.

Usage
-----

See :doc:`usage` for detailed usage instructions.

Features
--------

See :doc:`features` for a comprehensive list of features.

API Reference
-------------

See :doc:`api` for API documentation.

Contributing
------------

See :doc:`contributing` for contribution guidelines.

Changelog
---------

See :doc:`changelog` for version history.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
