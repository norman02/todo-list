import unittest
import tempfile
import os
import storage  # Import the module so we can override TASK_FILE
from tasks import add_task, remove_task, update_task
from storage import load_tasks, write_tasks

import tasks  # Access the global tasks list defined in tasks.py


class TestTasks(unittest.TestCase):
    def setUp(self):
        """Set up a temporary task file for testing and clear global tasks."""
        # Create a temporary file and save its name
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file = self.temp_file.name
        self.temp_file.close()  # Close it so that our code can read/write to it

        # Backup and override the TASK_FILE in storage module for testing
        self.original_file = storage.TASK_FILE
        storage.TASK_FILE = self.test_file

        # Clear the temporary file contents
        write_tasks([])

        # Reset the global tasks list in the tasks module
        tasks.tasks = []

    def tearDown(self):
        """Remove the temporary task file and restore the original TASK_FILE."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        storage.TASK_FILE = self.original_file

    def test_add_task(self):
        """Ensure tasks are added correctly."""
        result = add_task("Finish report", "HIGH", "2025-05-01")
        self.assertEqual(result, "Task added successfully!")
        current_tasks = load_tasks()
        self.assertIn("[HIGH] Finish report (Due: 2025-05-01)", current_tasks)

    def test_add_duplicate_task(self):
        """Ensure duplicate tasks are prevented."""
        add_task("Finish report", "HIGH", "2025-05-01")
        result = add_task("Finish report", "HIGH", "2025-05-01")
        self.assertEqual(result, "Task already exists!")

    def test_remove_task(self):
        """Ensure tasks are removed correctly."""
        add_task("Buy milk", "LOW")
        result = remove_task("Buy milk", "LOW")
        self.assertEqual(result, "Task removed successfully!")
        current_tasks = load_tasks()
        self.assertNotIn("[LOW] Buy milk", current_tasks)

    def test_update_task_priority(self):
        """Ensure task priority updates correctly."""
        add_task("Workout", "MEDIUM")
        result = update_task("Workout", "HIGH")
        self.assertEqual(result, "Task updated successfully!")
        current_tasks = load_tasks()
        self.assertIn("[HIGH] Workout", current_tasks)
        self.assertNotIn("[MEDIUM] Workout", current_tasks)

    def test_update_task_invalid_priority(self):
        """Ensure updating with an invalid priority fails."""
        add_task("Read book", "LOW")
        result = update_task("Read book", "INVALID")
        self.assertEqual(result, "Invalid priority level!")


if __name__ == "__main__":
    unittest.main()
