import unittest

import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.dirname(__file__) + "/..")
)  # Correct import path
from todo import add_task, view_tasks, update_task, process_recurring_tasks


class TestRecurringTasks(unittest.TestCase):
    def test_add_recurring_task(self):
        """Ensure recurring tasks are stored correctly"""
        result = add_task(
            "Exercise", priority="HIGH", due_date="2025-05-01", recurring="daily"
        )
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(
            "[HIGH] Exercise (Due: 2025-05-01) [Recurring: daily]", view_tasks()
        )

    def test_invalid_recurring_task(self):
        """Ensure invalid recurrence values are rejected."""
        result = add_task(
            "Yoga", priority="LOW", due_date="2025-06-10", recurring="yearly"
        )
        self.assertEqual(
            result, "Invalid recurrence type! Use 'daily', 'weekly', or 'monthly'."
        )

    def test_recurring_task_formatting(self):
        """Ensure reccuring tasks are formatted correctly"""
        add_task(
            "Running", priority="MEDIUM", due_date="2025-07-01", recurring="weekly"
        )
        self.assertIn(
            "[MEDIUM] Running (Due: 2025-07-01) [Recurring: weekly]", view_tasks()
        )

    def test_recurring_task_remains_after_update(self):
        """Ensure updating a recurring task does NOT remove recurrence label."""
        add_task(
            "Stretching", priority="HIGH", due_date="2025-05-01", recurring="daily"
        )  # Add recurring task
        update_task("Stretching", priority="MEDIUM")  # Modify priority only
        self.assertIn(
            "[MEDIUM] Stretching (Due: 2025-05-01) [Recurring: daily]", view_tasks()
        )  # Ensure recurrence persists

    def test_recurring_task_auto_generation(self):
        """Ensure past-due recurring tasks generate new instances with updated due dates."""
        add_task("Gym", priority="MEDIUM", due_date="2025-04-20", recurring="weekly")
        process_recurring_tasks()
        self.assertIn(
            "[MEDIUM] Gym (Due: 2025-04-27) [Recurring: weekly]", view_tasks()
        )

    def test_task_invalid_priority_and_recurring(self):
        """Ensure invalid priority and recurrence together trigger an error."""
        result = add_task(
            "Meditation", priority="UNKNOWN", due_date="2025-06-15", recurring="yearly"
        )
        self.assertEqual(result, "Invalid priority level or date format!")


if __name__ == "__main__":
    unittest.main()
