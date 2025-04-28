from datetime import datetime, timedelta
from storage import write_tasks


def process_recurring_tasks(tasks, today=None):
    """Checks past-due recurring tasks and generates new instances.

    Args:
        tasks (list): List of task strings.
        today (date, optional): The current date for comparison.
                                Defaults to datetime.today().date().
    """
    if today is None:
        today = datetime.today().date()
    new_tasks = []

    for task in tasks:
        if "[Recurring:" in task:
            task_parts = task.split("[Recurring: ")
            base_task = task_parts[0].strip()
            recurrence_type = task_parts[1][:-1]

            if " (Due: " in base_task:
                due_date_str = base_task.split(" (Due: ")[-1][:-1]
            else:
                continue  # No due date, skip processing

            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

            if due_date <= today:
                if recurrence_type == "daily":
                    new_due_date = due_date + timedelta(days=1)
                elif recurrence_type == "weekly":
                    new_due_date = due_date + timedelta(weeks=1)
                elif recurrence_type == "monthly":
                    if due_date.month == 12:
                        new_due_date = due_date.replace(year=due_date.year + 1, month=1)
                    else:
                        new_due_date = due_date.replace(month=due_date.month + 1)
                # If recurrence_type is unknown, new_due_date is never defined;
                # this will naturally raise an error, which our tests expect.
                new_task = f"{base_task.split(' (Due:')[0].strip()} (Due: {new_due_date}) [Recurring: {recurrence_type}]"
                new_tasks.append(new_task)

    tasks.extend(new_tasks)
    write_tasks(tasks)
