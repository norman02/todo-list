import unittest
import os
import storage  # Import the whole storage module
from storage import load_tasks, write_tasks  # Import the functions


class TestStorage(unittest.TestCase):
    def setUp(self):
        """Set up a temporary test file before each test."""
        self.test_file = "test_tasks.txt"
        # Backup original file reference from storage module
        self.original_file = storage.TASK_FILE
        # Override TASK_FILE in the storage module for testing
        storage.TASK_FILE = self.test_file

    def tearDown(self):
        """Cleanup after tests."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        # Restore the original TASK_FILE in storage
        storage.TASK_FILE = self.original_file

    def test_write_and_load_tasks(self):
        """Ensure tasks are saved and loaded correctly."""
        sample_tasks = ["[HIGH] Finish report", "[LOW] Buy milk"]
        write_tasks(sample_tasks)
        loaded_tasks = load_tasks()
        self.assertEqual(sample_tasks, loaded_tasks)

    def test_load_empty_file(self):
        """Ensure loading an empty file returns an empty list."""
        write_tasks([])  # Write an empty list
        loaded_tasks = load_tasks()
        self.assertEqual(loaded_tasks, [])


if __name__ == "__main__":
    unittest.main()
