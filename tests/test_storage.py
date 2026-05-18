import pathlib
import shutil
import tempfile
import unittest

import storage
from storage import load_highscore, save_highscore


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.original_file = storage.HIGHSCORE_FILE
        self.temp_dir = pathlib.Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "highscore.txt"
        storage.HIGHSCORE_FILE = self.test_file

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        storage.HIGHSCORE_FILE = self.original_file

    def test_load_no_file(self):
        """Should return 0 and create the file if it doesn't exist."""
        self.assertFalse(self.test_file.exists())
        self.assertEqual(load_highscore(), 0)
        self.assertTrue(self.test_file.exists())
        self.assertEqual(self.test_file.read_text(), "0")

    def test_save_and_load(self):
        """Should correctly save and load a score."""
        save_highscore(1234)
        self.assertEqual(load_highscore(), 1234)

    def test_load_corrupt_data(self):
        """Should return 0 if the file contains invalid data."""
        self.test_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_file.write_text("invalid")
        self.assertEqual(load_highscore(), 0)

    def test_load_empty_file(self):
        """Should return 0 if the file is empty."""
        self.test_file.parent.mkdir(parents=True, exist_ok=True)
        self.test_file.write_text("")
        self.assertEqual(load_highscore(), 0)

    def test_overwrite_highscore(self):
        """Should correctly update the score when saved again."""
        save_highscore(100)
        self.assertEqual(load_highscore(), 100)
        save_highscore(200)
        self.assertEqual(load_highscore(), 200)


if __name__ == '__main__':
    unittest.main()
