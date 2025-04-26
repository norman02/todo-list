import unittest
from todo import view_tasks, add_task, tasks


class TestReadTask(unittest.TestCase):
    def setUp(self):
        """Reset taks before each test."""
        global tasks
        tasks.clear()

    def test_view_tasks_empty_list(self):
        """Ensure view_tasks returns an empty list when no tasks exist."""
        self.assertEqual(view_tasks(), [])

    def test_view_tasks_with_tasks(self):
        """Ensure view_tasks displays the correct task list."""
        add_task("Submit project", priority="URGENT", due_date="2025-05-10")
        add_task("Buy groceries", priority="LOW")

        expected_tasks = [
            "[URGENT] Submit project (Due: 2025-05-10)",
            "[LOW] Buy groceries",
        ]
        self.assertEqual(view_tasks(), expected_tasks)
