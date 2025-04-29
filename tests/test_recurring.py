import unittest
from datetime import datetime, timedelta
from recurring import process_recurring_tasks


class TestRecurringTasks(unittest.TestCase):
    def setUp(self):
        """Monkey-patch write_tasks to avoid side effects and set common variables."""
        import recurring

        self.original_write_tasks = recurring.write_tasks
        # Override write_tasks so that it does nothing during tests.
        recurring.write_tasks = lambda tasks: None

        # Base tasks with various recurrence types.
        self.base_tasks = [
            "[HIGH] Finish report (Due: 2025-04-27) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-20) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-04-01) [Recurring: monthly]",
        ]
        # Fixed "today" used for most tests.
        self.fixed_today = datetime(2025, 4, 28).date()

    def tearDown(self):
        """Restore the original write_tasks."""
        import recurring

        recurring.write_tasks = self.original_write_tasks

    def test_empty_task_list(self):
        """An empty list should remain unchanged."""
        tasks = []
        process_recurring_tasks(tasks, today=self.fixed_today)
        self.assertEqual(tasks, [])

    def test_recurring_task_auto_generation(self):
        """
        Overdue or due-today tasks should trigger new tasks with updated due dates.
          - Daily: 2025-04-27 -> new task due 2025-04-28
          - Weekly: 2025-04-20 -> new task due 2025-04-27
          - Monthly: 2025-04-01 -> new task due 2025-05-01
        """
        tasks = self.base_tasks.copy()
        process_recurring_tasks(tasks, today=self.fixed_today)
        expected_tasks = [
            "[HIGH] Finish report (Due: 2025-04-28) [Recurring: daily]",
            "[MEDIUM] Weekly team sync (Due: 2025-04-27) [Recurring: weekly]",
            "[LOW] Pay rent (Due: 2025-05-01) [Recurring: monthly]",
        ]
        for expected in expected_tasks:
            self.assertIn(expected, tasks)

    def test_no_modification_for_future_tasks(self):
        """Tasks with due dates in the future should remain unchanged."""
        tasks = ["[URGENT] Project deadline (Due: 2050-05-10) [Recurring: weekly]"]
        process_recurring_tasks(tasks, today=self.fixed_today)
        self.assertEqual(
            tasks, ["[URGENT] Project deadline (Due: 2050-05-10) [Recurring: weekly]"]
        )

    def test_process_recurring_tasks_past_due(self):
        """For a daily task that is overdue, the new instance should have its due date advanced."""
        today = self.fixed_today
        yesterday = today - timedelta(days=1)
        tasks = [f"[MEDIUM] Review project (Due: {yesterday}) [Recurring: daily]"]
        process_recurring_tasks(tasks, today=today)
        # Expect the new daily task due date is yesterday + 1 day (i.e. equals today).
        self.assertIn(
            f"[MEDIUM] Review project (Due: {yesterday + timedelta(days=1)}) [Recurring: daily]",
            tasks,
        )

    def test_monthly_recurring_year_boundary(self):
        """A December monthly task should update to January of the next year."""
        tasks = ["[LOW] Pay credit card (Due: 2025-12-01) [Recurring: monthly]"]
        override_today = datetime(2025, 12, 2).date()
        process_recurring_tasks(tasks, today=override_today)
        self.assertIn(
            "[LOW] Pay credit card (Due: 2026-01-01) [Recurring: monthly]", tasks
        )

    def test_non_recurring_tasks_untouched(self):
        """Tasks without a recurring marker remain untouched."""
        tasks = ["[HIGH] Complete project (Due: 2025-04-27)"]
        original_tasks = tasks.copy()
        process_recurring_tasks(tasks, today=self.fixed_today)
        self.assertEqual(tasks, original_tasks)

    def test_invalid_due_date_format_raises_error(self):
        """Tasks with an invalid due date format should raise a ValueError."""
        tasks = ["[LOW] Invalid date task (Due: 2025/04/01) [Recurring: monthly]"]
        self.assertRaises(ValueError, process_recurring_tasks, tasks, self.fixed_today)

    def test_unknown_recurrence_type_raises_error(self):
        """Tasks with an unknown recurrence type should raise an error."""
        tasks = ["[LOW] Unknown recurrence (Due: 2025-04-01) [Recurring: yearly]"]
        self.assertRaises(ValueError, process_recurring_tasks, tasks, self.fixed_today)

    def test_today_parameter_override(self):
        """An explicit 'today' parameter should lead to correct updating of a daily task."""
        tasks = ["[HIGH] Task (Due: 2025-04-27) [Recurring: daily]"]
        override_today = datetime(2025, 4, 28).date()
        process_recurring_tasks(tasks, today=override_today)
        self.assertIn("[HIGH] Task (Due: 2025-04-28) [Recurring: daily]", tasks)

    def test_task_without_recurring_marker(self):
        """A task that does not have a recurring marker should be unchanged."""
        tasks = ["[MEDIUM] Standalone task (Due: 2025-04-01)"]
        original_tasks = tasks.copy()
        process_recurring_tasks(tasks, today=self.fixed_today)
        self.assertEqual(tasks, original_tasks)

    def test_default_today_parameter(self):
        """
        Ensure that when 'today' is None, the function defaults to the system's current date.
        We create a daily recurring task with a due date set to yesterday such that:
          new_due = (yesterday + 1 day) equals today's date.
        """
        system_today = datetime.today().date()
        yesterday = system_today - timedelta(days=1)
        task = f"[LOW] Example Task (Due: {yesterday}) [Recurring: daily]"
        tasks = [task]

        # Capture the expected new due date: yesterday + 1 day = system_today
        expected_new_due = system_today

        process_recurring_tasks(
            tasks, today=None
        )  # Let the function default to system today

        # Extract the due dates from processed tasks.
        processed_due_dates = [
            t.split("(Due: ")[-1].split(")")[0] for t in tasks if "(Due:" in t
        ]

        self.assertTrue(
            any(due_date == str(expected_new_due) for due_date in processed_due_dates),
            f"Expected new task due date to be {expected_new_due} when defaulting to system's today.",
        )

    def test_default_today_empty_tasks(self):
        """Ensure that 'today' is set to the system's date when None is provided, even with no tasks."""
        tasks = []
        # This call should execute the if branch because today is None.
        process_recurring_tasks(tasks, today=None)
        # If you want, you can verify that the branch printed the debug message
        # (e.g., by redirecting stdout), but even just calling this function forces the branch to run.
        self.assertEqual(tasks, [])


if __name__ == "__main__":
    unittest.main()
