from datetime import datetime

TASK_FILE = "task.txt"
VALID_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW"]


# Load tasks into an array at startup
def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


tasks = load_tasks()


def write_tasks():
    """Save the `tasks` array back to task.txt."""
    with open(TASK_FILE, "w") as file:
        file.writelines(f"{task}\n" for task in tasks)


def format_task(task, priority):
    """Format task with priority level."""
    return f"[{priority}] {task}"


def add_task(task, priority="MEDIUM", due_date=None):
    """Add a task with a priority level, preventing duplicates."""
    if priority not in VALID_PRIORITIES:
        return "Invalid priority level!"

    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()  # Validate format
        except ValueError:
            return "Invalid date format! Use YYYY-MM-DD."

    formatted_task = f"[{priority}] {task}" + (
        f" (Due: {due_date})" if due_date else ""
    )

    if formatted_task in tasks:
        return "Task already exists!"

    tasks.append(formatted_task)
    write_tasks()
    return "Task added successfully!"


def remove_task(task):
    """Remove a task by exact match, including priority formatting."""
    task_lower = task.lower()
    matching_tasks = [t for t in tasks if task_lower in t.lower()]

    if not matching_tasks:
        return "Task not found!"

    tasks.remove(matching_tasks[0])
    write_tasks()
    return "Task removed successfully!"


def view_tasks():
    """Return tasks sorted by priority level."""
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}

    return sorted(tasks, key=lambda t: priority_order.get(t.split("]")[0][1:], 99))
