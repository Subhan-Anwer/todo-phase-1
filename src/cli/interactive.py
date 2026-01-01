"""Main interactive module with mode detection and menu navigation."""

import sys
from typing import Optional
from rich.console import Console
from rich.table import Table

from ..models.task import Task
from ..services.todo_service import TodoService
from .menu import InteractiveSession

console = Console()
todo_service = TodoService()


def run_interactive_mode():
    """Run the interactive mode of the application."""
    session = InteractiveSession()

    while True:
        # Show main menu and get user selection
        selection = session.show_menu()

        if not selection or selection == "Quit":
            console.print("Goodbye! 👋")
            break

        # Handle user selection
        if selection == "Add Task":
            add_task_interactive()
        elif selection == "List Tasks":
            list_tasks_interactive()
        elif selection == "Complete Task":
            complete_task_interactive()
        elif selection == "Update Task":
            update_task_interactive()
        elif selection == "Delete Task":
            delete_task_interactive()

        # Pause to let user see the result before showing menu again
        console.input("\nPress Enter to continue...")


def add_task_interactive():
    """Interactive task addition with prompts."""
    try:
        title = console.input("Enter task title: ").strip()

        if not title:
            console.print("✗ Error: Task title cannot be empty", style="red")
            return

        description_input = console.input("Enter task description (optional, press Enter to skip): ").strip()
        description = description_input if description_input else None

        task = todo_service.add_task(title, description)
        console.print(f"✓ Task '{task.title}' added with ID {task.id}")

    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
    except KeyboardInterrupt:
        console.print("\n[X] Operation cancelled by user.", style="yellow")


def list_tasks_interactive():
    """Interactive task listing with formatted display."""
    try:
        tasks = todo_service.list_tasks()

        if not tasks:
            console.print("→ No tasks found")
            return

        table = Table("ID", "Status", "Title", "Description")
        for task in tasks:
            status = "✓" if task.completed else "✗"
            table.add_row(
                str(task.id),
                status,
                task.title,
                task.description or ""
            )
        console.print(table)

    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")


def complete_task_interactive():
    """Interactive task completion with selection."""
    try:
        tasks = todo_service.list_tasks()

        if not tasks:
            console.print("→ No tasks available to complete")
            return

        # Filter to show only incomplete tasks
        incomplete_tasks = [task for task in tasks if not task.completed]

        if not incomplete_tasks:
            console.print("→ No incomplete tasks to complete")
            return

        # Create menu options for incomplete tasks
        task_options = [f"Task {task.id}: {task.title}" for task in incomplete_tasks]
        task_options.append("Cancel")

        # Show task selection menu
        from simple_term_menu import TerminalMenu
        terminal_menu = TerminalMenu(
            task_options,
            title="Select a task to complete:",
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("bg_red", "fg_yellow"),
            cycle_cursor=True,
            clear_screen=False,
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index is None or task_options[menu_entry_index] == "Cancel":
            console.print("[X] Operation cancelled by user.", style="yellow")
            return

        # Get selected task ID
        selected_task = incomplete_tasks[menu_entry_index]

        success = todo_service.mark_complete(selected_task.id)
        if success:
            console.print(f"✓ Task {selected_task.id} marked as complete")
        else:
            console.print(f"✗ Error: Failed to mark task {selected_task.id} as complete", style="red")

    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")


def update_task_interactive():
    """Interactive task update with selection and prompts."""
    try:
        tasks = todo_service.list_tasks()

        if not tasks:
            console.print("→ No tasks available to update")
            return

        # Create menu options for all tasks
        task_options = [f"Task {task.id}: {task.title}" for task in tasks]
        task_options.append("Cancel")

        # Show task selection menu
        from simple_term_menu import TerminalMenu
        terminal_menu = TerminalMenu(
            task_options,
            title="Select a task to update:",
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("bg_red", "fg_yellow"),
            cycle_cursor=True,
            clear_screen=False,
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index is None or task_options[menu_entry_index] == "Cancel":
            console.print("[X] Operation cancelled by user.", style="yellow")
            return

        # Get selected task
        selected_task = tasks[menu_entry_index]

        # Get new values
        console.print(f"Current title: {selected_task.title}")
        new_title_input = console.input("Enter new title (press Enter to keep current): ").strip()
        new_title = new_title_input if new_title_input else None

        console.print(f"Current description: {selected_task.description or 'None'}")
        new_description_input = console.input("Enter new description (press Enter to keep current): ").strip()
        new_description = new_description_input if new_description_input else None

        # Only update if there's something to update
        if new_title is None and new_description is None:
            console.print("→ No changes made to the task")
            return

        # If we're updating the title to an empty string, use the current title
        if new_title == "":
            new_title = selected_task.title

        updated_task = todo_service.update_task(selected_task.id, new_title, new_description)
        if updated_task:
            console.print(f"✓ Task {selected_task.id} updated")
        else:
            console.print(f"✗ Error: Failed to update task {selected_task.id}", style="red")

    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")


def delete_task_interactive():
    """Interactive task deletion with selection and confirmation."""
    try:
        tasks = todo_service.list_tasks()

        if not tasks:
            console.print("→ No tasks available to delete")
            return

        # Create menu options for all tasks
        task_options = [f"Task {task.id}: {task.title}" for task in tasks]
        task_options.append("Cancel")

        # Show task selection menu
        from simple_term_menu import TerminalMenu
        terminal_menu = TerminalMenu(
            task_options,
            title="Select a task to delete:",
            menu_cursor="> ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("bg_red", "fg_yellow"),
            cycle_cursor=True,
            clear_screen=False,
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index is None or task_options[menu_entry_index] == "Cancel":
            console.print("[X] Operation cancelled by user.", style="yellow")
            return

        # Get selected task
        selected_task = tasks[menu_entry_index]

        # Confirm deletion
        confirm = console.input(f"Are you sure you want to delete task '{selected_task.title}'? (y/N): ").strip().lower()

        if confirm in ['y', 'yes']:
            success = todo_service.delete_task(selected_task.id)
            if success:
                console.print(f"✓ Task {selected_task.id} deleted")
            else:
                console.print(f"✗ Error: Failed to delete task {selected_task.id}", style="red")
        else:
            console.print("[X] Deletion cancelled by user.", style="yellow")

    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")


def detect_interactive_mode() -> bool:
    """Detect if the application should run in interactive mode based on arguments."""
    return len(sys.argv) == 1  # No arguments provided