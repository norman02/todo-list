import unittest
from format import format_task


class TestFormat(unittest.TestCase):
    def test_valid_task_format(self):
        """Ensure a task with valid inputs is formatted correctly."""
        result = format_task("Finish report", "HIGH", "2025-05-01", "daily")
        expected = "[HIGH] Finish report (Due: 2025-05-01) [Recurring: daily]"
        self.assertEqual(result, expected)

    def test_invalid_priority(self):
        """Ensure an invalid priority returns None."""
        result = format_task("Buy milk", "INVALID", "2025-05-01")
        self.assertIsNone(result)

    def test_invalid_date_format(self):
        """Ensure an incorrectly formatted date returns None."""
        result = format_task("Workout", "MEDIUM", "May 5, 2025")
        self.assertIsNone(result)

    def test_missing_due_date(self):
        """Ensure tasks without a due date format correctly."""
        result = format_task("Call John", "LOW")
        expected = "[LOW] Call John"
        self.assertEqual(result, expected)

    def test_missing_recurring(self):
        """Ensure tasks without a recurrence format correctly."""
        result = format_task("Read book", "MEDIUM", "2025-06-01")
        expected = "[MEDIUM] Read book (Due: 2025-06-01)"
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
