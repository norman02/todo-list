import unittest
from datetime import datetime
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


if __name__ == "__main__":
    unittest.main()
