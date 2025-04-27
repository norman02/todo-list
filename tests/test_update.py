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
