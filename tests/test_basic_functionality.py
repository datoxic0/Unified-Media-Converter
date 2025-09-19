"""
Basic functionality tests for Unified Media Converter v7
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestBasicFunctionality(unittest.TestCase):
    """Test basic functionality of the Unified Media Converter"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = Path(self.test_dir) / "test.txt"
        self.test_file.write_text("test content")
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        if self.test_file.exists():
            self.test_file.unlink()
        os.rmdir(self.test_dir)
    
    def test_import_main_module(self):
        """Test that the main module can be imported."""
        try:
            from unified_media_converter.src.unified_media_converter import main
            self.assertTrue(callable(main))
        except ImportError:
            self.fail("Failed to import main module")
    
    def test_version_info(self):
        """Test that version information is accessible."""
        try:
            from src import __version__, __author__
            self.assertIsInstance(__version__, str)
            self.assertIsInstance(__author__, str)
        except ImportError:
            self.fail("Failed to import version information")
    
    def test_file_operations(self):
        """Test basic file operations."""
        # Check that test file was created
        self.assertTrue(self.test_file.exists())
        
        # Check file content
        content = self.test_file.read_text()
        self.assertEqual(content, "test content")
    
    def test_path_operations(self):
        """Test path operations."""
        # Test that we can work with Path objects
        test_path = Path("test_file.txt")
        self.assertIsInstance(test_path, Path)
        
        # Test basic path properties
        self.assertEqual(test_path.name, "test_file.txt")
        self.assertEqual(test_path.suffix, ".txt")

if __name__ == '__main__':
    unittest.main()
