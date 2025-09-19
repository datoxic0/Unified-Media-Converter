# Changelog

All notable changes to the Unified Media Converter project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-19

### Added
- Comprehensive video-to-video conversion capabilities
- Support for MP4, AVI, MKV, MOV, WMV, FLV, WebM formats
- Video quality/bitrate options with codec selection (libx264, libx265, vp9, copy)
- Enhanced audio-to-audio conversion with MP3, AAC, FLAC, WAV, M4A, OGG, WMA support
- Batch processing queue with real-time progress tracking
- Parametric EQ editor with visualization
- A/B comparison and crossfade audition features
- FIR coefficient export (CSV, .f32 raw, IR WAV for FFmpeg afir)
- Preset management system
- Drag-and-drop file support
- Keyboard shortcuts for improved workflow
- Detailed logging and error reporting

### Changed
- Complete UI overhaul with modern, intuitive interface
- Improved DSP algorithms for better audio quality
- Enhanced threading model for smoother performance
- Better error handling and recovery mechanisms
- Optimized memory usage for large file processing
- Updated documentation with comprehensive user guide

### Fixed
- Various stability improvements
- Memory leaks in long-running processes
- UI responsiveness during intensive operations
- File handling edge cases
- Compatibility issues with different FFmpeg versions

## [6.0.0] - 2025-08-15

### Added
- Initial release with basic audio conversion capabilities
- Parametric EQ editor with multi-band support
- FFmpeg integration for audio processing
- Basic file queue management
- Simple visualization of frequency response

### Changed
- Foundation for future video processing capabilities
- Modular architecture for easy expansion
- Basic UI layout for core functionality

[Unreleased]: https://github.com/unified-media-converter/unified-media-converter/compare/v7.0.0...HEAD
[7.0.0]: https://github.com/unified-media-converter/unified-media-converter/releases/tag/v7.0.0
[6.0.0]: https://github.com/unified-media-converter/unified-media-converter/releases/tag/v6.0.0
