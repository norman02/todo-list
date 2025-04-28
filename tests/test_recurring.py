import unittest
from datetime import datetime, timedelta
from recurring import process_recurring_tasks


class TestRecurringTasks(unittest.TestCase):
    def setUp(self):
        """Set up common tasks for tests."""
        self.base_tasks = [
            "[HIGH] Finish report (Due: 2025-04-27) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-20) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-04-01) [Recurring: monthly]",
        ]

    def test_recurring_task_auto_generation(self):
        """Ensure past-due recurring tasks generate new instances with updated due dates."""
        tasks = self.base_tasks.copy()
        process_recurring_tasks(tasks)
        expected_tasks = [
            "[HIGH] Finish report (Due: 2025-04-28) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-27) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-05-01) [Recurring: monthly]",
        ]
        for expected in expected_tasks:
            self.assertIn(expected, tasks)

    def test_no_modification_for_future_tasks(self):
        """Ensure future recurring tasks remain unchanged."""
        tasks = ["[URGENT] Project deadline (Due: 2025-05-10) [Recurring: weekly]"]
        process_recurring_tasks(tasks)
        self.assertEqual(
            tasks, ["[URGENT] Project deadline (Due: 2025-05-10) [Recurring: weekly]"]
        )

    def test_process_recurring_tasks_past_due(self):
        """Ensure past-due recurring tasks update correctly using the current date logic."""
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        tasks = [
            f"[MEDIUM] Review project (Due: {yesterday}) [Recurring: daily]",
            f"[LOW] Pay rent (Due: {yesterday}) [Recurring: monthly]",
        ]
        process_recurring_tasks(tasks)
        # The daily task should update to yesterday + 1 day (i.e. today).
        self.assertIn(
            f"[MEDIUM] Review project (Due: {today}) [Recurring: daily]", tasks
        )
        # For the monthly task, determine the expected next-month date.
        if yesterday.month == 12:
            expected_next_month = yesterday.replace(year=yesterday.year + 1, month=1)
        else:
            expected_next_month = yesterday.replace(month=yesterday.month + 1)
        self.assertIn(
            f"[LOW] Pay rent (Due: {expected_next_month}) [Recurring: monthly]", tasks
        )

    def test_no_due_date_skips_processing(self):
        """Ensure tasks without a due date are skipped (line 19)."""
        tasks = ["[MEDIUM] Task without due date [Recurring: daily]"]
        original_tasks = tasks.copy()
        process_recurring_tasks(tasks)
        self.assertEqual(
            tasks, original_tasks, "Tasks without a due date should not be processed."
        )

    def test_monthly_recurring_year_boundary(self):
        """Ensure monthly recurring tasks correctly transition from December to January."""
        tasks = ["[LOW] Pay credit card (Due: 2025-12-01) [Recurring: monthly]"]
        # Override 'today' so that the due date is considered past due.
        override_today = datetime(2025, 12, 2).date()
        process_recurring_tasks(tasks, today=override_today)
        self.assertIn(
            "[LOW] Pay credit card (Due: 2026-01-01) [Recurring: monthly]", tasks
        )

    def test_non_recurring_tasks_untouched(self):
        """Ensure tasks without a [Recurring: substring remain unchanged."""
        tasks = ["[HIGH] Complete project (Due: 2025-04-27)"]
        original_tasks = tasks.copy()
        process_recurring_tasks(tasks)
        self.assertEqual(
            tasks, original_tasks, "Non-recurring tasks should remain unchanged."
        )

    def test_invalid_due_date_format_raises_error(self):
        """Ensure tasks with an invalid due date format raise a ValueError."""
        tasks = ["[LOW] Invalid date task (Due: 2025/04/01) [Recurring: monthly]"]
        with self.assertRaises(ValueError):
            process_recurring_tasks(tasks)

    def test_invalid_recurrence_type_raises_error(self):
        """Ensure tasks with an unknown recurrence type raise an error.

        This test expects that if no valid branch exists for the recurrence type,
        then attempting to construct the new task leads to an error.
        """
        tasks = ["[LOW] Unknown recurrence (Due: 2025-04-01) [Recurring: yearly]"]
        with self.assertRaises(UnboundLocalError):
            process_recurring_tasks(tasks)

    def test_today_parameter_override(self):
        """Test process_recurring_tasks with an explicit 'today' parameter override."""
        tasks = ["[HIGH] Task (Due: 2025-04-27) [Recurring: daily]"]
        fixed_today = datetime(2025, 4, 28).date()
        process_recurring_tasks(tasks, today=fixed_today)
        self.assertIn("[HIGH] Task (Due: 2025-04-28) [Recurring: daily]", tasks)

    def test_empty_task_list(self):
        """Ensure an empty task list remains unchanged."""
        tasks = []
        process_recurring_tasks(tasks)
        self.assertEqual(tasks, [], "Empty taks list should remain empty")


if __name__ == "__main__":
    unittest.main()
