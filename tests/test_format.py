import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from format import format_task
from config import VALID_PRIORITIES, VALID_RECURRENCES


class TestFormat(unittest.TestCase):
    def test_valid_task_format_all_fields(self):
        """Test valid task formatting with all fields provided."""
        result = format_task("Finish report", "HIGH", "2025-05-01", "daily")
        expected = "[HIGH] Finish report (Due: 2025-05-01) [Recurring: daily]"
        self.assertEqual(result, expected)

    def test_valid_task_format_only_due_date(self):
        """Test valid formatting with a task and due_date only."""
        result = format_task("Call John", "LOW", "2025-05-15")
        expected = "[LOW] Call John (Due: 2025-05-15)"
        self.assertEqual(result, expected)

    def test_valid_task_format_only_task(self):
        """Test valid formatting when only a task name is provided."""
        result = format_task("Read book", "MEDIUM")
        expected = "[MEDIUM] Read book"
        self.assertEqual(result, expected)

    def test_invalid_priority(self):
        """Ensure an invalid priority returns None."""
        result = format_task("Buy milk", "CRITICAL", "2025-05-01")
        self.assertIsNone(result)

    def test_invalid_date_format(self):
        """Ensure an incorrectly formatted date returns None."""
        result = format_task("Workout", "MEDIUM", "May 5, 2025")
        self.assertIsNone(result)

    def test_invalid_recurring_format(self):
        """Ensure an invalid recurring value returns None."""
        result = format_task("Morning run", "MEDIUM", "2025-05-01", "everyday")
        self.assertIsNone(result)

    def test_empty_task_name(self):
        """Ensure an empty task name returns None."""
        result = format_task("", "HIGH", "2025-07-01")
        self.assertIsNone(result)

    def test_whitespace_task_name(self):
        """Ensure a task name with only spaces returns None."""
        result = format_task("   ", "LOW", "2025-07-01")
        self.assertIsNone(result)

    def test_lowercase_priority(self):
        """Ensure lowercase priorities are normalized."""
        result = format_task("Lunch meeting", "medium", "2025-07-15")
        expected = "[MEDIUM] Lunch meeting (Due: 2025-07-15)"
        self.assertEqual(result, expected)

    def test_special_characters_task_name(self):
        """Ensure task names with special characters are formatted correctly."""
        result = format_task("Meeting @ 3PM!", "URGENT", "2025-09-01")
        expected = "[URGENT] Meeting @ 3PM! (Due: 2025-09-01)"
        self.assertEqual(result, expected)

    def test_extreme_future_due_date(self):
        """Ensure a very distant future due date formats correctly."""
        result = format_task("Future project", "HIGH", "2100-01-01")
        expected = "[HIGH] Future project (Due: 2100-01-01)"
        self.assertEqual(result, expected)

    def test_extreme_past_due_date(self):
        """Ensure a very old past due date formats correctly."""
        result = format_task("History exam", "MEDIUM", "1900-12-31")
        expected = "[MEDIUM] History exam (Due: 1900-12-31)"
        self.assertEqual(result, expected)

    def test_due_date_none(self):
        """Test behavior when due_date is explicitly None but recurrence is provided."""
        result = format_task("No deadline task", "LOW", None, "weekly")
        expected = "[LOW] No deadline task [Recurring: weekly]"
        self.assertEqual(result, expected)

    def test_recurring_none(self):
        """Test behavior when recurring is explicitly None."""
        result = format_task("Task without recurrence", "MEDIUM", "2025-06-15", None)
        expected = "[MEDIUM] Task without recurrence (Due: 2025-06-15)"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
