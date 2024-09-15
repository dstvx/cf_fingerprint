import unittest
from pathlib import Path
from cf_fingerprint import get_fingerprint

class TestFingerprint(unittest.TestCase):
    def test_small_file(self):
        # Test with a small file example
        file_path = Path('test_files/small_file.txt')
        result = get_fingerprint(file_path)
        self.assertIsInstance(result, int)

    def test_large_file(self):
        # Test with a large file example
        file_path = Path('test_files/large_file.bin')
        result = get_fingerprint(file_path)
        self.assertIsInstance(result, int)

    def test_file_not_found(self):
        # Test with a non-existent file
        file_path = Path('non_existent_file.txt')
        result = get_fingerprint(file_path)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
