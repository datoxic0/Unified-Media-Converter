"""
pytest configuration file for Unified Media Converter tests
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# pytest configuration
def pytest_configure(config):
    """Configure pytest settings."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

# Fixture for temporary directories
import pytest
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

# Fixture for sample media files
@pytest.fixture
def sample_audio_file(temp_dir):
    """Create a sample audio file for tests."""
    import wave
    import struct
    
    # Create a simple WAV file with a sine wave
    sample_rate = 44100
    duration = 1  # 1 second
    frequency = 440  # A4 note
    
    samples = []
    for i in range(int(sample_rate * duration)):
        sample = 32767 * 0.5 * math.sin(2 * math.pi * frequency * i / sample_rate)
        samples.append(struct.pack('<h', int(sample)))
    
    filename = Path(temp_dir) / "sample.wav"
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(samples))
    
    return filename

# Import math for the sample file fixture
import math
