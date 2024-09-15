import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import tempfile
from pathlib import Path
from cf_fingerprint import get_fingerprint

class TestFingerprint(unittest.TestCase):
    def test_small_file(self):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write("Hello, World!")
            temp_file.flush()
            temp_file_path = Path(temp_file.name)

        try:
            result = get_fingerprint(temp_file_path)
            self.assertIsInstance(result, int)
        finally:
            temp_file_path.unlink()  # Ensure file is deleted after test

    def test_large_file(self):
        with tempfile.NamedTemporaryFile(mode='wb+', delete=False) as temp_file:
            temp_file.write(b'a' * 1_000_000)  # 1MB file
            temp_file.flush()
            temp_file_path = Path(temp_file.name)

        try:
            result = get_fingerprint(temp_file_path)
            self.assertIsInstance(result, int)
        finally:
            temp_file_path.unlink()  # Ensure file is deleted after test

    def test_file_not_found(self):
        non_existent_file = Path(tempfile.gettempdir()) / 'non_existent_file.txt'
        result = get_fingerprint(non_existent_file)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()