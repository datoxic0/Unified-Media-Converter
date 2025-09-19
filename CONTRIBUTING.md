# Contributing to Unified Media Converter

Thank you for your interest in contributing to Unified Media Converter! We welcome contributions from the community to help improve this open-source project.

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please check if the issue has already been reported. If not, create a new issue with:

1. A clear and descriptive title
2. A detailed description of the problem
3. Steps to reproduce the issue
4. Expected behavior vs. actual behavior
5. Screenshots if applicable
6. Your operating system and version
7. FFmpeg version
8. Python version

### Suggesting Enhancements

We welcome suggestions for new features or improvements. Please create an issue with:

1. A clear and descriptive title
2. A detailed explanation of the proposed enhancement
3. Use cases and benefits
4. Any implementation ideas you might have

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/unified-media-converter.git
   cd unified-media-converter
   ```
3. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Setup

1. Install Python 3.8 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install FFmpeg (see README.md for instructions)

#### Coding Standards

1. Follow PEP 8 style guide for Python code
2. Use meaningful variable and function names
3. Write docstrings for all public functions and classes
4. Add type hints where appropriate
5. Keep functions small and focused
6. Write unit tests for new functionality

#### Testing

1. Ensure all existing tests pass
2. Add new tests for any functionality you add
3. Test your changes on multiple platforms if possible
4. Verify compatibility with different FFmpeg versions

#### Submitting Changes

1. Run the application to ensure your changes work as expected
2. Update the README.md if you've added or changed functionality
3. Add yourself to the contributors list if desired
4. Commit your changes with a clear and descriptive commit message
5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
6. Create a pull request with:
   - A clear title
   - Detailed description of changes
   - Reference to any related issues

## Development Guidelines

### Architecture Overview

The application follows a modular design:

1. **Core Processing**: FFmpeg-based media processing
2. **UI Layer**: Tkinter-based graphical interface
3. **DSP Engine**: Digital signal processing for EQ and FIR filters
4. **Worker Threads**: Asynchronous processing for file conversions
5. **Configuration**: JSON-based preset and settings management

### Key Components

1. **UnifiedApp**: Main application class managing UI and coordination
2. **Worker**: Thread class handling individual conversion tasks
3. **Band**: Data class representing EQ bands
4. **Task**: Data class representing queued conversion jobs
5. **DSP Functions**: Mathematical functions for EQ design and FIR processing

### Best Practices

1. **Error Handling**: Always handle exceptions gracefully
2. **Resource Management**: Properly clean up temporary files and resources
3. **Threading**: Use thread-safe patterns for UI updates
4. **Logging**: Provide informative logs for debugging
5. **Performance**: Optimize for large files and batch processing
6. **Compatibility**: Maintain cross-platform support

## Code of Conduct

This project adheres to a code of conduct that promotes respectful and inclusive interactions. By participating, you are expected to uphold this standard.

## Questions?

If you have any questions about contributing, feel free to:

1. Open an issue for discussion
2. Contact the maintainers directly
3. Join our community discussions (if available)

Thank you for helping make Unified Media Converter better!
