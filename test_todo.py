import unittest, os, todo
from todo import add_task, remove_task, view_tasks, load_tasks, write_tasks, tasks

# 🔹 Centralized Test Data
TEST_DATA = {
    "task_name": "Finish homework",
    "priority_levels": ["URGENT", "HIGH", "MEDIUM", "LOW"],
    "invalid_priority": "INVALID",
    "valid_due_date": "2025-05-01",
    "invalid_due_date": "May 5, 2025",
}


class TestTodo(unittest.TestCase):
    def setUp(self):
        """Reset tasks before each test to avoid contamination."""
        global tasks
        tasks.clear()

    def test_add_task(self):
        """Test adding a new task with default priority."""
        result = add_task(TEST_DATA["task_name"])
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(f"[MEDIUM] {TEST_DATA['task_name']}", tasks)

    def test_add_task_with_priority(self):
        """Ensure tasks are added with priority levels."""
        for priority in TEST_DATA["priority_levels"]:
            with self.subTest(priority=priority):
                result = add_task(TEST_DATA["task_name"], priority)
                self.assertEqual(result, "Task added successfully!")
                self.assertIn(f"[{priority}] {TEST_DATA['task_name']}", tasks)

    def test_add_task_with_deadline(self):
        """Ensure tasks can be added with a deadline."""
        result = add_task(
            TEST_DATA["task_name"],
            priority="HIGH",
            due_date=TEST_DATA["valid_due_date"],
        )
        self.assertEqual(result, "Task added successfully!")
        self.assertIn(
            f"[HIGH] {TEST_DATA['task_name']} (Due: {TEST_DATA['valid_due_date']})",
            tasks,
        )

    def test_add_task_invalid_priority(self):
        """Ensure invalid priority input is rejected."""
        result = add_task(
            TEST_DATA["task_name"], priority=TEST_DATA["invalid_priority"]
        )
        self.assertEqual(result, "Invalid priority level!")

    def test_add_task_invalid_date_format(self):
        """Ensure incorrect date formats are handled properly."""
        result = add_task(
            TEST_DATA["task_name"],
            priority="HIGH",
            due_date=TEST_DATA["invalid_due_date"],
        )
        self.assertEqual(result, "Invalid date format! Use YYYY-MM-DD.")

    def test_prevent_duplicate_tasks(self):
        """Ensure duplicate tasks are prevented."""
        add_task(TEST_DATA["task_name"])
        result = add_task(TEST_DATA["task_name"])
        self.assertEqual(result, "Task already exists!")

    def test_remove_task(self):
        """Test removing a task by exact match."""
        add_task(TEST_DATA["task_name"], priority="MEDIUM")

        global tasks
        tasks = view_tasks()
        self.assertIn(f"[MEDIUM] {TEST_DATA['task_name']}", tasks)

        result = remove_task(TEST_DATA["task_name"])
        self.assertEqual(result, "Task removed successfully!")

        tasks = view_tasks()
        self.assertNotIn(f"[MEDIUM] {TEST_DATA['task_name']}", tasks)

    def test_remove_nonexistent_task(self):
        """Ensure removing a non-existent task returns an error."""
        result = remove_task("Nonexistent Task")
        self.assertEqual(result, "Task not found!")

    def test_remove_task_case_insensitive(self):
        """Ensure removing a task works case-insensitively."""
        add_task("Write Report", priority="HIGH")

        result = remove_task("write report")  # Testing lowercase input
        self.assertEqual(result, "Task removed successfully!")
        self.assertNotIn("[HIGH] Write Report", tasks)

    def test_load_tasks_missing_file(self):
        """Ensure task loading handles missing file gracefully."""
        global tasks

        # Temporarily overited TASK_FILE for this test

        original_file = todo.TASK_FILE
        todo.TASK_FILE = "invalid.txt"  # Use a non-existant file
        try:
            tasks = load_tasks()
            self.assertIsInstance(tasks, list)  # should return a list even if empty
            self.assertEqual(
                tasks, []
            )  # If no file exists, it should return an empty list
        finally:
            todo.TASK_FILE = original_file  # Restore the correct file

    def test_view_tasks_empty_list(self):
        """Ensure view_tasks returns an empty list when no tasks exist."""
        global tasks
        tasks.clear()
        self.assertEqual(view_tasks(), [])

    def test_view_tasks_with_tasks(self):
        """Ensure view_tasks displays the correct task list."""
        global tasks
        tasks.clear()

        add_task("Submit project", priority="URGENT", due_date="2025-05-10")
        add_task("Buy groceries", priority="LOW")

        expected_tasks = [
            "[URGENT] Submit project (Due: 2025-05-10)",
            "[LOW] Buy groceries",
        ]
        self.assertEqual(view_tasks(), expected_tasks)

    def test_write_tasks_saves_data(self):
        """Ensure write_tasks correctly saves tasks."""
        global tasks
        tasks.clear()

        add_task("Clean the house", priority="MEDIUM")
        write_tasks()

        new_tasks = load_tasks()
        self.assertIn("[MEDIUM] Clean the house", new_tasks)


def test_view_tasks_sorted_by_priority(self):
    """Ensure tasks are sorted correctly by priority."""
    global tasks
    tasks.clear()

    # Add tasks in random order
    add_task("Buy groceries", priority="LOW")
    add_task("Complete project", priority="URGENT")
    add_task("Submit assignment", priority="HIGH")
    add_task("Attend meeting", priority="MEDIUM")

    expected_order = [
        "[URGENT] Complete project",
        "[HIGH] Submit assignment",
        "[MEDIUM] Attend meeting",
        "[LOW] Buy groceries",
    ]

    self.assertEqual(view_tasks(), expected_order)


def test_remove_task_with_similar_names(self):
    """Ensure remove_task correctly removes only the exact match."""
    global tasks
    tasks.clear()

    # Add tasks with similar names
    add_task("Finish homework", priority="HIGH")
    add_task("Finish math homework", priority="LOW")

    result = remove_task("Finish homework")

    self.assertEqual(result, "Task removed successfully!")
    self.assertNotIn("[HIGH] Finish homework", tasks)  # Task should be gone
    self.assertIn("[LOW] Finish math homework", tasks)  # This should remain


def test_add_task_with_valid_due_date(self):
    """Ensure tasks can be added with a valid due date."""
    global tasks
    tasks.clear()

    result = add_task("Prepare report", priority="HIGH", due_date="2025-06-15")

    self.assertEqual(result, "Task added successfully!")
    self.assertIn("[HIGH] Prepare report (Due: 2025-06-15)", tasks)


def test_remove_nonexistent_task(self):
    """Ensure removing a non-existent task returns an error message."""
    global tasks
    tasks.clear()

    result = remove_task("Unfinished project")  # Task does not exist

    self.assertEqual(result, "Task not found!")  # Should return expected error message


def test_view_tasks_empty_list(self):
    """Ensure view_tasks returns an empty list when no tasks exist."""
    global tasks
    tasks.clear()

    result = view_tasks()
    self.assertEqual(
        result, []
    )  # Should return an empty list when no tasks are present


def test_view_tasks_sorted_correctly(self):
    """Ensure tasks are sorted by priority correctly."""
    global tasks
    tasks.clear()

    # Adding tasks in mixed order
    add_task("A - Low priority task", priority="LOW")
    add_task("B - Urgent task", priority="URGENT")
    add_task("C - High priority task", priority="HIGH")
    add_task("D - Medium priority task", priority="MEDIUM")

    expected_order = [
        "[URGENT] B - Urgent task",
        "[HIGH] C - High priority task",
        "[MEDIUM] D - Medium priority task",
        "[LOW] A - Low priority task",
    ]

    result = view_tasks()
    self.assertEqual(
        result, expected_order
    )  # Should return tasks sorted in correct order


def test_write_tasks_saves_data(self):
    """Ensure write_tasks correctly saves tasks to task.txt."""
    global tasks
    tasks.clear()

    # Add a test task
    add_task("Clean the kitchen", priority="HIGH")
    write_tasks()

    # Read the file to confirm it's saved
    with open("task.txt", "r") as file:
        saved_tasks = [line.strip() for line in file.readlines()]

    self.assertIn("[HIGH] Clean the kitchen", saved_tasks)


def test_add_empty_task(self):
    """Ensure adding an empty task name is rejected."""
    global tasks
    tasks.clear()

    result = add_task("")  # Attempt to add an empty task
    self.assertEqual(result, "Task name cannot be empty!")


def test_format_task(self):
    """Ensure tasks are formatted correctly with priority."""
    formatted_task = format_task("Complete project", "HIGH")

    self.assertEqual(formatted_task, "[HIGH] Complete project")  # Expected format


import os


def test_load_tasks_malformed_file(self):
    """Ensure load_tasks handles malformed task files properly."""
    global tasks

    # Create a corrupted file for testing
    with open("task.txt", "w") as file:
        file.write("CORRUPTED DATA\n[HIGH] Valid task\n???")

    tasks = load_tasks()

    # Expected: It should at least load valid tasks while ignoring corrupted ones
    self.assertIn("[HIGH] Valid task", tasks)
    self.assertNotIn("CORRUPTED DATA", tasks)  # Should ignore bad data
    self.assertNotIn("???", tasks)  # Invalid lines should be skipped


def test_remove_task_with_extra_spaces(self):
    """Ensure remove_task correctly trims leading and trailing spaces."""
    global tasks
    tasks.clear()

    # Add a task with normal spacing
    add_task("Finish homework", priority="MEDIUM")

    # Try removing with extra spaces
    self.assertEqual(remove_task("  Finish homework"), "Task removed successfully!")

    # Re-add and test trailing space
    add_task("Finish homework", priority="MEDIUM")
    self.assertEqual(remove_task("Finish homework  "), "Task removed successfully!")

    # Ensure task is truly gone
    self.assertNotIn("[MEDIUM] Finish homework", tasks)


def test_add_task_with_extra_spaces(self):
    """Ensure add_task trims leading/trailing spaces correctly."""
    global tasks
    tasks.clear()

    result = add_task("  Finish homework  ")
    self.assertEqual(result, "Task added successfully!")
    self.assertIn(
        "[MEDIUM] Finish homework", tasks
    )  # Spaces should be trimmed in stored task name


def test_add_task_with_duplicate_spaces(self):
    """Ensure tasks with duplicate spaces in the middle are stored correctly."""
    global tasks
    tasks.clear()

    result = add_task("Do  homework", priority="HIGH")  # Two spaces in the middle
    self.assertEqual(result, "Task added successfully!")
    self.assertIn(
        "[HIGH] Do  homework", tasks
    )  # Should store exactly as entered, with spaces intact


def test_add_task_with_numeric_name(self):
    """Ensure numeric task names are handled properly."""
    global tasks
    tasks.clear()

    result = add_task("Task 101", priority="LOW")
    self.assertEqual(result, "Task added successfully!")
    self.assertIn("[LOW] Task 101", tasks)  # Numbers should be handled correctly


if __name__ == "__main__":
    unittest.main()
