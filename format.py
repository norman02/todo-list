from datetime import datetime

VALID_PRIORITIES = ["URGENT", "HIGH", "MEDIUM", "LOW"]


def format_task(task, priority, due_date=None, recurring=None):
    """Format a task string with priority, due date, and recurrence."""
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
        formatted_task += f" [Recurring: {recurring}]"

    return formatted_task
