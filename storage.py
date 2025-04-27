TASK_FILE = "task.txt"


def load_tasks():
    """Load tasks from file."""
    try:
        with open(TASK_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def write_tasks(tasks):
    """Save tasks to file."""
    with open(TASK_FILE, "w") as file:
        file.writelines(f"{task}\n" for task in tasks)
