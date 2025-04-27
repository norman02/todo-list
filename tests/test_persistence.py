import os
import unittest
from todo import load_tasks, TASK_FILE


class TestPersistence(unittest.TestCase):
    def setUp(self):
        """Ensure the task file doesn't exist before each test."""
        if os.path.exists(TASK_FILE):
            os.remove(TASK_FILE)

    def test_load_tasks_file_not_found(self):
        """Ensure function handles missing file gracefully."""
        self.assertEqual(load_tasks(), [])

    def tearDown(self):
        """Restore the task file after test execution."""
        with open(TASK_FILE, "w") as file:
            file.write("")  # Reset file for future tests


if __name__ == "__main__":
    unittest.main()  # pragma: no cover
