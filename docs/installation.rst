Installation Guide
=================

This guide will help you install and set up Unified Media Converter v7 on your system.

Prerequisites
-------------

Before installing Unified Media Converter v7, ensure you have the following prerequisites:

1. **Python 3.8 or higher** - Download from `python.org <https://www.python.org/downloads/>`_
2. **FFmpeg and FFprobe** - Available from `ffmpeg.org <https://ffmpeg.org/download.html>`_
3. **Git** (optional) - For cloning the repository from `git-scm.com <https://git-scm.com/downloads>`_

System Requirements
-------------------

Unified Media Converter v7 is designed to work on:

- **Windows 10/11** (64-bit recommended)
- **macOS 10.15 or higher** (Catalina and later)
- **Linux distributions** (Ubuntu 20.04+, Fedora 32+, Debian 11+, etc.)

Hardware Requirements
^^^^^^^^^^^^^^^^^^^^^

- **CPU**: Intel i5 or AMD Ryzen 5 equivalent or better (for video processing)
- **RAM**: 8GB minimum (16GB recommended for large file processing)
- **Storage**: 500MB free space for application (additional space for media files)
- **Display**: 1920x1080 resolution or higher recommended

Installing FFmpeg
-----------------

FFmpeg is required for all media processing operations in Unified Media Converter v7.

Windows
^^^^^^^

Option 1: Using Chocolatey (recommended)
""""""""""""""""

If you have Chocolatey installed:

.. code-block:: bash

   choco install ffmpeg

Option 2: Manual Installation
"""""""""""""""""""""

1. Download FFmpeg from `gyan.dev <https://www.gyan.dev/ffmpeg/builds/>`_ or `BtbN <https://github.com/BtbN/FFmpeg-Builds/releases>`_
2. Extract the archive to a folder (e.g., ``C:\ffmpeg``)
3. Add the ``bin`` directory to your system PATH:
   
   a. Open System Properties → Advanced → Environment Variables
   b. Edit the PATH variable and add ``C:\ffmpeg\bin``
   c. Restart your command prompt or PowerShell

Verify the installation:

.. code-block:: bash

   ffmpeg -version
   ffprobe -version

macOS
^^^^^

Using Homebrew (recommended):

.. code-block:: bash

   brew install ffmpeg

Linux (Ubuntu/Debian)
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo apt update
   sudo apt install ffmpeg

Linux (Fedora/RHEL/CentOS)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   sudo dnf install ffmpeg

Installing Python Dependencies
------------------------------

Unified Media Converter v7 requires several Python packages. You can install them using pip:

Required Dependencies
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   pip install ffmpeg-python numpy matplotlib simpleaudio tkinterdnd2

Optional Dependencies (Recommended)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For enhanced functionality and better performance:

.. code-block:: bash

   pip install scipy pillow pygame

Installing Unified Media Converter v7
------------------------------------

Option 1: Direct Download
^^^^^^^^^^^^^^^^^^^^^^^^^

1. Download the latest version from the releases page
2. Extract the archive to your preferred location
3. Run the application:

.. code-block:: bash

   python unified_media_converter.py

Option 2: Clone from Repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you prefer to work with the source code:

.. code-block:: bash

   git clone https://github.com/unified-media-converter/unified-media-converter.git
   cd unified-media-converter
   pip install -r requirements.txt

Verifying Installation
----------------------

To verify that everything is installed correctly:

1. Open a terminal or command prompt
2. Navigate to the directory containing ``unified_media_converter_v7.py``
3. Run the application:

.. code-block:: bash

   python unified_media_converter.py

If the application starts without errors, your installation is successful.

Troubleshooting
---------------

Common Issues and Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^

FFmpeg Not Found
""""""""""""""""

**Problem**: Error message indicating FFmpeg is not in PATH

**Solution**: 
1. Verify FFmpeg installation location
2. Add FFmpeg's bin directory to your system PATH
3. Restart your terminal/command prompt
4. Verify with ``ffmpeg -version``

Missing Python Packages
""""""""""""""

**Problem**: ImportError when running the application

**Solution**:
1. Install missing packages with pip:

.. code-block:: bash

   pip install -r requirements.txt

Permission Denied
"""""""""""""""""

**Problem**: Permission errors when running the application

**Solution**:
1. On Unix-like systems, make the script executable:

.. code-block:: bash

   chmod +x unified_media_converter.py

2. Or run with Python explicitly:

.. code-block:: bash

   python unified_media_converter.py

GUI Not Displaying Properly
"""""""""""""""""""

**Problem**: Missing visual elements or distorted UI

**Solution**:
1. Install optional GUI dependencies:

.. code-block:: bash

   pip install numpy matplotlib tkinterdnd2

2. If issues persist, try installing system-specific GUI libraries:

Windows:

.. code-block:: bash

   pip install pywin32

macOS:

.. code-block:: bash

   brew install python-tk

Linux:

.. code-block:: bash

   sudo apt install python3-tk

Additional Resources
--------------------

- `FFmpeg Documentation <https://ffmpeg.org/documentation.html>`_
- `Python Documentation <https://docs.python.org/>`_
- `NumPy Documentation <https://numpy.org/doc/>`_
- `Matplotlib Documentation <https://matplotlib.org/stable/index.html>`_

For further assistance, please check the project's GitHub issues or contact support.
