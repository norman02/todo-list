import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import unittest
from datetime import datetime, timedelta
from recurring import process_recurring_tasks


class TestRecurringTasks(unittest.TestCase):
    def setUp(self):
        """Set up test tasks before each test."""
        self.tasks = [
            "[HIGH] Finish report (Due: 2025-04-27) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-20) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-04-01) [Recurring: monthly]",
        ]

    def test_recurring_task_auto_generation(self):
        """Ensure past-due recurring tasks generate new instances with updated due dates."""
        process_recurring_tasks(self.tasks)

        # Expected updated tasks
        expected_tasks = [
            "[HIGH] Finish report (Due: 2025-04-28) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-27) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-05-01) [Recurring: monthly]",
        ]

        for expected in expected_tasks:
            self.assertIn(expected, self.tasks)

    def test_no_modification_for_future_tasks(self):
        """Ensure future recurring tasks remain unchanged."""
        future_tasks = [
            "[URGENT] Project deadline (Due: 2025-05-10) [Recurring: weekly]"
        ]
        process_recurring_tasks(future_tasks)

        self.assertEqual(
            future_tasks,
            ["[URGENT] Project deadline (Due: 2025-05-10) [Recurring: weekly]"],
        )

    def test_process_recurring_tasks_past_due(self):
        """Ensure past-due recurring tasks update correctly."""
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)

        tasks = [
            f"[MEDIUM] Review project (Due: {yesterday}) [Recurring: daily]",
            f"[LOW] Pay rent (Due: {yesterday}) [Recurring: monthly]",
        ]

        process_recurring_tasks(tasks)

        # new tasks should be created with updated due dats

        self.assertIn(
            f"[MEDIUM] Review project (Due: {today}) [Recurring: daily]", tasks
        )
        expected_next_month = yesterday.replace(month=yesterday.month + 1)
        self.assertIn(
            f"[LOW] Pay rent (Due: {expected_next_month}) [Recurring: monthly]", tasks
        )

    def test_process_recurring_tasks_no_due_date(self):
        """Ensure tasks without a due date are skipped."""
        tasks = [
            "[MEDIUM] Read book [Recurring: daily]",  # ❌ No due date!
            "[HIGH] Team meeting (Due: 2025-04-01) [Recurring: weekly]",  # ✅ Has a due date
        ]

        process_recurring_tasks(tasks)

        # The task WITHOUT a due date should remain unchanged

        self.assertIn("[MEDIUM] Read book [Recurring: daily]", tasks)

        # The task WITH a due date should be processed correctly
        self.assertIn(
            "[HIGH] Team meeting (Due: 2025-04-08) [Recurring: weekly]", tasks
        )  # Example updated date

    def test_no_due_date_skips_processing(self):
        """Ensure that a recurring task without a due date is skipped (line 19)."""
        # This task does not include " (Due: " in the base part.
        tasks = ["[MEDIUM] Task without due date [Recurring: daily]"]
        original_tasks = tasks.copy()
        process_recurring_tasks(tasks)
        # Since there's no due date, the task should remain unchanged
        self.assertEqual(
            tasks, original_tasks, "Task without due date should not be processed."
        )


if __name__ == "__main__":
    unittest.main()
