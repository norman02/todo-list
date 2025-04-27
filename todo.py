from datetime import datetime, timedelta

TASK_FILE = "task.txt"
VALID_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW"]


# Load tasks into an array at startup
from storage import load_tasks, write_tasks

tasks = load_tasks()

from storage import write_tasks as save_tasks  # Give it a clear alias


def format_task(task, priority, due_date=None, recurring=None):
    """
    Create a formatted task string.
    Returns None if priority is invalid or if the due_date is malformed.
    """
    if priority not in VALID_PRIORITIES:
        return None

    formatted_task = f"[{priority}] {task}"
    if due_date:
        try:
            due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
            formatted_task += f" (Due: {due_date_parsed})"
        except ValueError:
            return None

    if recurring:
        # We assume recurring is validated already.
        formatted_task += f" [Recurring: {recurring}]"
    return formatted_task


def add_task(task, priority="MEDIUM", due_date=None, recurring=None):
    """
    Add a task with an optional due date and recurrence.
    Returns error messages matching test expectations.
    """
    if recurring is not None:
        if priority not in VALID_PRIORITIES:
            return "Invalid priority level or date format!"

    if recurring is not None and recurring.lower() not in [
        "daily",
        "weekly",
        "monthly",
    ]:
        return "Invalid recurrence type! Use 'daily', 'weekly', or 'monthly'."
    formatted_task = format_task(task, priority, due_date, recurring)
    if formatted_task is None:
        return "Invalid priority level or date format!"
    if formatted_task in tasks:
        return "Task already exists!"
    tasks.append(formatted_task)
    save_tasks(tasks)
    return "Task added successfully!"


def remove_task(task_name, priority=None):
    """Remove a task by exact match of name and priority."""
    global tasks
    if priority:
        matching_tasks = [t for t in tasks if f"[{priority}] {task_name}" in t]
    else:
        matching_tasks = [
            t
            for t in tasks
            if task_name.lower() == t.split("] ")[-1].split(" (Due:")[0].strip().lower()
        ]
    if not matching_tasks:
        return "Task not found!"
    tasks.remove(matching_tasks[0])
    save_tasks(tasks)
    return "Task removed successfully!"


def view_tasks():
    """Process recurring tasks and return sorted task list."""
    process_recurring_tasks()  # Auto-generate upcoming recurring tasks
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}
    # Sort by priority (using the number order) and then alphabetically.
    return sorted(tasks, key=lambda t: (priority_order.get(t.split("]")[0][1:], 99), t))


def update_task(task_name, priority=None, due_date=None):
    """
    Update a given task's priority or due date while preserving any recurrence.
    Returns messages that match the expected test output.
    """
    global tasks
    for i, task in enumerate(tasks):
        try:
            idx_bracket = task.index("] ")
        except ValueError:
            continue
        rest = task[idx_bracket + 2 :]
        if " (Due:" in rest:
            current_task_name = rest.split(" (Due:")[0].strip().lower()
        else:
            current_task_name = rest.strip().lower()
        if task_name.lower() == current_task_name:
            # Extract current priority.
            try:
                current_priority = task[1 : task.index("]")]
            except ValueError:
                current_priority = "MEDIUM"
            # Extract due date if present.
            if " (Due: " in task:
                idx_start = task.find(" (Due: ") + len(" (Due: ")
                idx_end = task.find(")", idx_start)
                current_due_date = task[idx_start:idx_end]
            else:
                current_due_date = None
            # Extract recurring value if present.
            if "[Recurring: " in task:
                idx_r_start = task.find("[Recurring: ") + len("[Recurring: ")
                idx_r_end = task.find("]", idx_r_start)
                current_recurring = task[idx_r_start:idx_r_end]
            else:
                current_recurring = None
            # Determine new priority.
            new_priority = priority.upper() if priority else current_priority
            if priority and new_priority not in VALID_PRIORITIES:
                return "Invalid priority level!"
            # Determine new due date.
            if due_date:
                try:
                    due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
                except ValueError:
                    return "Invalid date format! Use YYYY-MM-DD."
                new_due_date = f" (Due: {due_date_parsed})"
            else:
                new_due_date = f" (Due: {current_due_date})" if current_due_date else ""
            # Preserve the recurring tag (only appended once).
            new_recurring = (
                f" [Recurring: {current_recurring}]" if current_recurring else ""
            )
            tasks[i] = f"[{new_priority}] {task_name}{new_due_date}{new_recurring}"
            save_tasks(tasks)
            return "Task updated successfully!"
    return "Task not found!"


def process_recurring_tasks():
    """
    Check tasks for recurrence. For each recurring task with a due date in the past
    or today, auto-generate a new instance with an updated due date.
    """
    today = datetime.today().date()
    new_tasks = []
    for task in tasks:
        if "[Recurring:" in task:
            task_parts = task.split("[Recurring: ")
            base_task = task_parts[0].strip()
            recurrence_type = task_parts[1][:-1]  # Remove the trailing ']'
            if " (Due: " in base_task:
                idx_start = base_task.find(" (Due: ") + len(" (Due: ")
                idx_end = base_task.find(")", idx_start)
                due_date_str = base_task[idx_start:idx_end]
            else:
                due_date_str = None
            if due_date_str:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_date <= today:
                    if recurrence_type == "daily":
                        new_due_date = due_date + timedelta(days=1)
                    elif recurrence_type == "weekly":
                        new_due_date = due_date + timedelta(weeks=1)
                    elif recurrence_type == "monthly":
                        try:
                            new_due_date = due_date.replace(month=due_date.month + 1)
                        except ValueError:
                            # Handle end-of-year rollover:
                            new_due_date = due_date.replace(
                                year=due_date.year + 1, month=1
                            )

                    # Remove any existing due date before adding a new one
                    base_task_cleaned = base_task.split(" (Due:")[0].strip()
                    new_task = f"{base_task_cleaned} (Due: {new_due_date}) [Recurring: {recurrence_type}]"
                    new_tasks.append(new_task)
    tasks.extend(new_tasks)
    save_tasks(tasks)
