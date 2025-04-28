from format import format_task
from storage import write_tasks, load_tasks
from recurring import process_recurring_tasks
from storage import load_tasks
from config import VALID_PRIORITIES  # Import constants

tasks = load_tasks()  # Load tasks at startup


def view_tasks():
    """Process recurring tasks and return sorted task list."""
    process_recurring_tasks()  # Auto-generate upcoming recurring tasks
    tasks = load_tasks()  # Load updated task list
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}
    # Sort by priority (using the predefined order) and then alphabetically.
    return sorted(tasks, key=lambda t: (priority_order.get(t.split("]")[0][1:], 99), t))


def add_task(task, priority="MEDIUM", due_date=None, recurring=None):
    """Add a task with priority, optional due date, and recurrence."""
    formatted_task = format_task(task, priority, due_date, recurring)
    if formatted_task is None:
        return "Invalid priority level or date format!"
    if formatted_task in tasks:
        return "Task already exists!"
    tasks.append(formatted_task)
    write_tasks(tasks)
    return "Task added successfully!"


def remove_task(task_name, priority=None):
    """Remove a task by exact match."""
    global tasks
    matching_tasks = (
        [t for t in tasks if f"[{priority}] {task_name}" in t]
        if priority
        else [t for t in tasks if task_name.lower() in t.lower()]
    )
    if not matching_tasks:
        return "Task not found!"
    tasks.remove(matching_tasks[0])
    write_tasks(tasks)
    return "Task removed successfully!"


def update_task(task_name, priority=None, due_date=None):
    """Update a task’s priority or due date while preserving recurrence."""
    global tasks
    for i, task in enumerate(tasks):
        if f"] {task_name}" in task:  # Ensure name matches
            old_priority = task[1 : task.index("]")]  # Extract priority
            new_priority = priority.upper() if priority else old_priority

            if priority and new_priority not in ["URGENT", "HIGH", "MEDIUM", "LOW"]:
                return "Invalid priority level!"

            new_due_date = None
            if due_date:
                try:
                    new_due_date = (
                        f" (Due: {datetime.strptime(due_date, '%Y-%m-%d').date()})"
                    )
                except ValueError:
                    return "Invalid date format!"

            if " (Due:" in task:
                task_name = task.split(" (Due:")[0].strip()

            recurring_tag = ""
            if "[Recurring:" in task:
                recurring_tag = f" {task.split('[Recurring:')[-1]}"

            tasks[i] = (
                f"[{new_priority}] {task_name}{new_due_date or ''}{recurring_tag}"
            )
            write_tasks(tasks)
            return "Task updated successfully!"

    return "Task not found!"
