from datetime import datetime, timedelta
from storage import write_tasks, load_tasks


def process_recurring_tasks(tasks=None, today=None):
    """
    Process recurring tasks:
      - If a recurring task has a due date that is <= today,
        generate a new instance with an updated due date.

    For recurrence types:
      - daily: advance by 1 day
      - weekly: advance by 7 days
      - monthly: advance by one month (with December rolling over to January)

    Args:
      tasks (list): List of task strings.
      today (date, optional): Override for current date. Defaults to today.
    """
    if today is None:
        today = datetime.today().date()

    if tasks is None:
        tasks = load_tasks()  # Load tasks when no argment is provided

    new_tasks = []

    for task in tasks:
        if "[Recurring:" not in task:
            continue

        # Assume task format is: "[PRIORITY] Task description (Due: YYYY-MM-DD) [Recurring: type]"
        try:
            # Split into the part before the recurring sign and the recurrence info
            task_parts = task.split("[Recurring:")
            base_task = task_parts[0].strip()  # contains the description and due date
            recurrence_field = (
                task_parts[1].rstrip("] ").strip()
            )  # e.g. "daily", "weekly", or "monthly"
        except IndexError:
            # If parsing fails, just skip the task.
            continue

        recurrence_type = recurrence_field

        # Extract due date from the base task. We assume due date is in the format (Due: YYYY-MM-DD)
        if " (Due:" not in base_task:
            continue  # No due date found; skip

        try:
            due_part = base_task.split(" (Due: ")[-1]  # e.g. "2025-04-27)"
            due_date_str = due_part.rstrip(")")
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except Exception:
            raise ValueError("Invalid due date format.")

        # Validate recurrence type.
        VALID_RECURRENCES = ["daily", "weekly", "monthly"]
        if recurrence_type not in VALID_RECURRENCES:
            raise ValueError(f"Unknown recurrence type: {recurrence_type}")

        # If the task is due (or overdue), update it.
        if due_date <= today:
            if recurrence_type == "daily":
                new_due = due_date + timedelta(days=1)
            elif recurrence_type == "weekly":
                new_due = due_date + timedelta(weeks=1)
            elif recurrence_type == "monthly":
                if due_date.month == 12:
                    new_due = due_date.replace(year=due_date.year + 1, month=1)
                else:
                    # This simplistic advance assumes the day exists in the next month.
                    new_due = due_date.replace(month=due_date.month + 1)
            # Generate the new task string with the updated due date.
            new_task = f"{base_task.split(' (Due:')[0].strip()} (Due: {new_due}) [Recurring: {recurrence_type}]"
            new_tasks.append(new_task)

    tasks.extend(new_tasks)
    write_tasks(tasks)
