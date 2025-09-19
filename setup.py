"""
Setup script for Unified Media Converter
"""

from setuptools import setup, find_packages
from pathlib import Path

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name="unified-media-converter",
    version="1.0.0",
    description="Professional audio and video converter with advanced parametric EQ capabilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/unified-media-converter/unified-media-converter",
    author="Siyabonga Blessing Phakathi",
    author_email="datoxic0@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 5 - Production/Stable",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        "ffmpeg-python>=0.2.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "simpleaudio>=1.0.0",
        "tkinterdnd2>=0.3.0",
    ],
    entry_points={
        "console_scripts": [
            "unified-media-converter=unified_media_converter.__main__:main",
        ]
    },
    python_requires=">=3.8",
    keywords=["media", "converter", "audio", "video", "ffmpeg", "eq", "equalizer", "dsp"],
    project_urls={
        "Bug Reports": "https://github.com/unified-media-converter/unified-media-converter/issues",
        "Documentation": "https://github.com/unified-media-converter/unified-media-converter/blob/main/README.md",
        "Source": "https://github.com/unified-media-converter/unified-media-converter",
    },
)
