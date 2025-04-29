import unittest
from unittest.mock import patch
from todo import main


class TestTodoMain(unittest.TestCase):

    @patch(
        "todo.view_tasks", return_value=["[HIGH] Write report", "[LOW] Submit invoice"]
    )
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "5"])
    def test_view_tasks(self, mock_input, mock_print, mock_view_tasks):
        """
        Test the 'View Tasks' branch:
          - User chooses option '1' to view tasks.
          - The patched 'view_tasks' returns a known list.
          - Then the user exits by choosing '5'.
        Verify that the output displays the header and each task.
        """
        main()

        # Ensure view_tasks is called.
        mock_view_tasks.assert_called_once()

        # Collect all printed messages.
        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertIn("\n📜 Task List:", printed_lines)
        self.assertTrue(any(" - [HIGH] Write report" in line for line in printed_lines))
        self.assertTrue(
            any(" - [LOW] Submit invoice" in line for line in printed_lines)
        )

    @patch("todo.add_task", return_value="Task added successfully!")
    @patch("builtins.print")
    @patch(
        "builtins.input",
        side_effect=["2", "Finish project", "HIGH", "2025-05-01", "daily", "5"],
    )
    def test_add_task(self, mock_input, mock_print, mock_add_task):
        """
        Test the 'Add Task' branch:
          - User chooses option '2', then enters task details.
          - The patched add_task returns a success message.
          - The user then exits.
        Verify that add_task is called with proper parameters and the success message is printed.
        """
        main()

        # Verify that add_task was called once with the expected parameters.
        mock_add_task.assert_called_once_with(
            "Finish project", "HIGH", "2025-05-01", "daily"
        )

        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(
            any("✅ Task added successfully!" in line for line in printed_lines)
        )

    @patch("todo.remove_task", return_value="Task removed successfully!")
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "Finish project", "HIGH", "5"])
    def test_remove_task(self, mock_input, mock_print, mock_remove_task):
        """
        Test the 'Remove Task' branch:
          - User selects option '3' and then enters the task name and its priority.
          - The patched remove_task returns a success message.
          - The user then exits.
        Verify that remove_task is called with the expected parameters
        and the corresponding message is printed.
        """
        main()

        mock_remove_task.assert_called_once_with("Finish project", "HIGH")

        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(
            any("✅ Task removed successfully!" in line for line in printed_lines)
        )

    @patch("todo.update_task", return_value="Task updated successfully!")
    @patch("builtins.print")
    @patch(
        "builtins.input", side_effect=["4", "Finish project", "HIGH", "2025-06-01", "5"]
    )
    def test_update_task(self, mock_input, mock_print, mock_update_task):
        """
        Test the 'Update Task' branch:
          - User selects option '4', then enters the task name, new priority, and new due date.
          - The patched update_task returns a success message.
          - The user finally exits.
        Verify that update_task is called with the correct parameters and the message is printed.
        """
        main()

        mock_update_task.assert_called_once_with("Finish project", "HIGH", "2025-06-01")

        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(
            any("✅ Task updated successfully!" in line for line in printed_lines)
        )

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["7", "5"])
    def test_invalid_choice(self, mock_input, mock_print):
        """
        Test the invalid choice handling:
          - User enters an invalid option (e.g., "7") then exits.
        Verify that the error message about invalid choice is printed.
        """
        main()

        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(
            any(
                "⚠ Invalid choice! Please enter a number between 1-5." in line
                for line in printed_lines
            )
        )

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["5"])
    def test_exit(self, mock_input, mock_print):
        """
        Test the exit branch:
          - User simply selects option '5' to exit.
        Verify that the exit message is printed.
        """
        main()

        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(
            any("👋 Exiting Task Manager. Goodbye!" in line for line in printed_lines)
        )


if __name__ == "__main__":
    unittest.main()
