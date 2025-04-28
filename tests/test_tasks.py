import unittest
import tempfile
import os
import storage  # Import the full storage module to override TASK_FILE
from tasks import add_task, remove_task, update_task
from storage import load_tasks, write_tasks


class TestTasks(unittest.TestCase):
    def setUp(self):
        """Set up a temporary task file for testing."""
        # Create a temporary file and get its name:
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.test_file = self.temp_file.name
        self.temp_file.close()  # Close the file so that it can be accessed later

        # Backup and override the TASK_FILE in storage module:
        self.original_file = storage.TASK_FILE
        storage.TASK_FILE = self.test_file

        # Clear the temporary test file:
        write_tasks([])

    def tearDown(self):
        """Remove the temporary file and restore the original TASK_FILE."""
        os.remove(self.test_file)
        storage.TASK_FILE = self.original_file

    def test_add_task(self):
        """Ensure tasks are added correctly."""
        result = add_task("Finish report", "HIGH", "2025-05-01")
        self.assertEqual(result, "Task added successfully!")
        tasks = load_tasks()
        self.assertIn("[HIGH] Finish report (Due: 2025-05-01)", tasks)

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
        tasks = load_tasks()
        self.assertNotIn("[LOW] Buy milk", tasks)

    def test_update_task_priority(self):
        """Ensure task priority updates correctly."""
        add_task("Workout", "MEDIUM")
        result = update_task("Workout", "HIGH")
        self.assertEqual(result, "Task updated successfully!")
        tasks = load_tasks()
        self.assertIn("[HIGH] Workout", tasks)
        self.assertNotIn("[MEDIUM] Workout", tasks)

    def test_update_task_invalid_priority(self):
        """Ensure updating with an invalid priority fails."""
        add_task("Read book", "LOW")
        result = update_task("Read book", "INVALID")
        self.assertEqual(result, "Invalid priority level!")


if __name__ == "__main__":
    unittest.main()
