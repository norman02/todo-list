import unittest
from todo import remove_task, view_tasks, add_task, tasks


class TestDeleteTask(unittest.TestCase):
    def setUp(self):
        """Reset tasks before each test."""
        global tasks
        tasks.clear()

    def test_remove_task(self):
        """Test removing a task by exact match."""
        add_task("Finish homework", priority="MEDIUM")
        self.assertIn("[MEDIUM] Finish homework", view_tasks())

        result = remove_task("Finish homework")
        self.assertEqual(result, "Task removed successfully!")
        self.assertNotIn("[MEDIUM] Finish homework", view_tasks())

    def test_remove_nonexistent_task(self):
        """Ensure removing a non-existent task returns an error."""
        result = remove_task("Nonexistent Task")
        self.assertEqual(result, "Task not found!")
