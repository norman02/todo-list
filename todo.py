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


def format_task(task, priority, due_date=None):
    """Format a task string with a priority and an optional due date."""
    if priority not in VALID_PRIORITIES:
        return None

    formatted_task = f"[{priority}] {task}"
    if due_date:
        try:
            # Validate and parse the date
            due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
            formatted_task += f" (Due: {due_date_parsed})"
        except ValueError:
            return None
    return formatted_task


def add_task(task, priority="MEDIUM", due_date=None):
    """Add a task with a priority level, preventing duplicates."""
    formatted_task = format_task(task, priority, due_date)
    if formatted_task is None:
        return "Invalid priority level or date format!"

    if formatted_task in tasks:
        return "Task already exists!"

    tasks.append(formatted_task)
    write_tasks()
    return "Task added successfully!"


def remove_task(task_name, priority=None):
    """Remove a task by exact match of both name and priority."""
    global tasks

    matching_tasks = (
        [t for t in tasks if f"[{priority}] {task_name}" in t]
        if priority
        else [
            t
            for t in tasks
            if task_name.lower() == t.split("] ")[-1].split(" (Due:")[0].strip().lower()
        ]
    )

    if not matching_tasks:
        return "Task not found!"

    tasks.remove(matching_tasks[0])
    write_tasks()

    return "Task removed successfully!"


def view_tasks():
    """Return tasks sorted by priority (based on a defined order) and then alphabetically."""
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}
    return sorted(tasks, key=lambda t: (priority_order.get(t.split("]")[0][1:], 99), t))


def update_task(task_name, priority=None, due_date=None):
    """Update an existing task's priority or due date with exact task name matching."""
    global tasks
    for i, task in enumerate(tasks):
        # Extract the task name from the stored task string
        current_task_name = task.split("] ")[-1].split(" (Due:")[0].strip().lower()
        if task_name.lower() == current_task_name:
            # Get current priority and due date (if any)
            current_priority = task.split("]")[0][1:]
            current_due_date = (
                task.split("(Due: ")[-1][:-1] if "(Due:" in task else None
            )

            # Validate the new priority if provided
            if priority and priority.upper() not in VALID_PRIORITIES:
                return "Invalid priority level!"

            # Validate and parse the new due date if provided
            if due_date:
                try:
                    due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    return "Invalid date format! Use YYYY-MM-DD."

            new_priority = priority.upper() if priority else current_priority
            new_due_date = (
                f" (Due: {due_date_parsed})"
                if due_date
                else (f" (Due: {current_due_date})" if current_due_date else "")
            )

            # Update task using the original task name (to preserve exact naming)
            tasks[i] = f"[{new_priority}] {task_name}{new_due_date}"
            write_tasks()
            return "Task updated successfully!"

    return "Task not found!"
