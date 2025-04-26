import unittest
from todo import add_task, view_tasks, remove_task, tasks

TEST_DATA = {
    "task_name": "Finish homework",
    "priority": "HIGH",
    "due_date": "2025-05-01",
}


class TestCreateTask(unittest.TestCase):
    def setUp(self):
        """Reset tasks before each test"""
        global tasks
        tasks.clear()

    def test_add_task_success(self):
        """Ensure a new task is added correctly."""
        result = add_task(TEST_DATA["task_name"])
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(f"[MEDIUM] {TEST_DATA['task_name']}", view_tasks())

    def test_add_task_with_priority(self):
        """Ensure tasks are added with correct priority levels."""
        result = add_task(TEST_DATA["task_name"], TEST_DATA["priority"])
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(
            f"[{TEST_DATA['priority']}] {TEST_DATA['task_name']}", view_tasks()
        )

    def test_add_task_with_deadline(self):
        """Ensure tasks can be added with deadlines."""
        result = add_task(
            TEST_DATA["task_name"], priority="HIGH", due_date=TEST_DATA["due_date"]
        )
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(
            f"[HIGH] {TEST_DATA['task_name']} (Due: {TEST_DATA['due_date']})",
            view_tasks(),
        )
