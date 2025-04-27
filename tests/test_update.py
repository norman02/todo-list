import unittest
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.dirname(__file__) + "/..")
)  # ✅ Correct import path
from todo import add_task, view_tasks, remove_task, update_task, tasks


class TestUpdateTask(unittest.TestCase):
    def setUp(self):
        """Reset tasks before each test."""
        global tasks
        tasks.clear()

    def test_update_task_priority(self):
        """Ensure task priority can be updated."""
        add_task("Finish homework", priority="LOW")
        update_task("Finish homework", priority="HIGH")
        self.assertIn("[HIGH] Finish homework", view_tasks())

    def test_update_task_deadline(self):
        """Ensure task deadline can be updated."""
        add_task("Submit project", priority="MEDIUM")
        update_task("Submit project", due_date="2025-06-01")
        self.assertIn("[MEDIUM] Submit project (Due: 2025-06-01)", view_tasks())

    def test_update_invalid_priority(self):
        """Ensure updating a task with an invalid priority fails."""
        add_task("Prepare slides")  # First, add a valid task
        result = update_task("Prepare slides", priority="RANDOM")  # Invalid priority
        self.assertEqual(result, "Invalid priority level!")

    def test_update_invalid_date(self):
        """Ensure updating a task with a malformed date fails."""
        add_task("Submit report")  # First, add a valid task
        result = update_task("Submit report", due_date="31-Feb-2025")  # Invalid date
        self.assertEqual(result, "Invalid date format! Use YYYY-MM-DD.")

    def test_update_task_invalid_date_format(self):
        """Ensure updating a task with a malformed due date fails."""
        add_task("Write book")  # First, add a valid task
        result = update_task("Write book", due_date="2025-13-45")  # Invalid date
        self.assertEqual(result, "Invalid date format! Use YYYY-MM-DD.")

    def test_update_task_preserve_existing_due_date(self):
        """Ensure updating priority preserves the existing due date correctly."""
        add_task(
            "Write novel", priority="MEDIUM", due_date="2025-06-01"
        )  # Create a task with a due date
        result = update_task(
            "Write novel", priority="HIGH"
        )  # Change priority but keep existing due date
        self.assertEqual(result, "Task updated successfully!")
        self.assertIn(
            "[HIGH] Write novel (Due: 2025-06-01)", view_tasks()
        )  # Verify due date remains

    def test_update_task_preserve_due_date(self):
        """Ensure updating priority does NOT remove an existing due date."""
        add_task(
            "Write novel", priority="MEDIUM", due_date="2025-06-01"
        )  # Create a task with a due date
        result = update_task(
            "Write novel", priority="HIGH"
        )  # Change priority but keep due date
        self.assertEqual(result, "Task updated successfully!")
        self.assertIn(
            "[HIGH] Write novel (Due: 2025-06-01)", view_tasks()
        )  # Verify due date remains

    def test_update_task_not_found(self):
        """Ensure updating a non-existent task returns 'Task not found!'"""
        # No task "Nonexistent Task" has been added.
        result = update_task("Nonexistent Task", priority="HIGH")
        self.assertEqual(result, "Task not found!")
