from tasks import add_task, remove_task, update_task, view_tasks
from config import TASK_FILE


def main():
    while True:
        print("\n📌 Task Manager")
        print("[1] View Tasks")
        print("[2] Add Task")
        print("[3] Remove Task")
        print("[4] Update Task")
        print("[5] Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            tasks = view_tasks()
            print("\n📜 Task List:")
            for task in tasks:
                print(f" - {task}")

        elif choice == "2":
            name = input("Task name: ")
            priority = input("Priority (URGENT/HIGH/MEDIUM/LOW): ").upper()
            due_date = input("Due date (YYYY-MM-DD, optional): ") or None
            recurring = input("Recurring (daily/weekly/monthly, optional): ") or None

            result = add_task(name, priority, due_date, recurring)
            print(f"✅ {result}")

        elif choice == "3":
            name = input("Task to remove: ")
            priority = input("Priority (or press Enter to skip): ") or None
            result = remove_task(name, priority)
            print(f"✅ {result}")

        elif choice == "4":
            name = input("Task to update: ")
            priority = input("New priority (or press Enter to skip): ") or None
            due_date = input("New due date (YYYY-MM-DD, optional): ") or None
            result = update_task(name, priority, due_date)
            print(f"✅ {result}")

        elif choice == "5":
            print("👋 Exiting Task Manager. Goodbye!")
            break

        else:
            print("⚠ Invalid choice! Please enter a number between 1-5.")


if __name__ == "__main__":
    main()
