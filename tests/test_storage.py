import unittest
import os
from storage import load_tasks, write_tasks
from config import TASK_FILE


class TestStorage(unittest.TestCase):
    def setUp(self):
        """Ensure TASK_FILE starts empty before each test."""
        with open(TASK_FILE, "w") as file:
            file.truncate(0)

    def tearDown(self):
        """Clean up TASK_FILE after each test."""
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)

    def test_load_tasks_empty_file(self):
        """Ensure an empty file returns an empty list."""
        self.assertEqual(load_tasks(), [])

    def test_load_tasks_missing_file(self):
        """Ensure a missing file returns an empty list gracefully."""
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)
        self.assertEqual(load_tasks(), [])

    def test_write_tasks_and_load(self):
        """Ensure tasks are written to and retrieved correctly."""
        tasks = ["[HIGH] Finish report", "[LOW] Buy groceries"]
        write_tasks(tasks)
        self.assertEqual(load_tasks(), tasks)


if __name__ == "__main__":
    unittest.main()
