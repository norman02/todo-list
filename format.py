from datetime import datetime
from config import VALID_PRIORITIES, VALID_RECURRENCES


def format_task(task, priority, due_date=None, recurring=None):
    """Format a task string with priority, due date, and recurrence."""

    if priority.upper() not in VALID_PRIORITIES:
        return None  # Ensure priority is valid

    if not task.strip():  # Fix: Ensure no blank or whitespace-only names
        return None

    priority = priority.upper()  # Normalize priority input

    formatted_task = f"[{priority}] {task}"

    if due_date:
        try:
            due_date_parsed = datetime.strptime(due_date, "%Y-%m-%d").date()
            formatted_task += f" (Due: {due_date_parsed})"
        except ValueError:
            return None  # Invalid date format handling

    if recurring:
        if recurring.lower() not in VALID_RECURRENCES:  # Fix: Validate recurring input
            return None
        formatted_task += f" [Recurring: {recurring.lower()}]"

    return formatted_task
