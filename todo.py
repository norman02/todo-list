from datetime import datetime, timedelta

TASK_FILE = "task.txt"
VALID_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW"]


# Load tasks into an array at startup
from storage import load_tasks, write_tasks

tasks = load_tasks()

from storage import write_tasks as save_tasks  # Give it a clear alias
from format import format_task

from tasks impoart add_task, remove_task, update_task


def view_tasks():
    """Process recurring tasks and return sorted task list."""
    process_recurring_tasks()  # Auto-generate upcoming recurring tasks
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}
    # Sort by priority (using the number order) and then alphabetically.
    return sorted(tasks, key=lambda t: (priority_order.get(t.split("]")[0][1:], 99), t))



from recurring import process_recurring_tasks
