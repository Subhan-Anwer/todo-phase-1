import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from ..models.task import Task
from ..services.todo_service import TodoService

app = typer.Typer()
console = Console()
todo_service = TodoService()


def display_tasks(tasks):
    """Display tasks in a formatted table"""
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


@app.command()
def add(title: str, description: Optional[str] = typer.Argument(None, help="Optional description for the task")):
    """Add a new task with optional description"""
    try:
        # Validate title
        if not title or not title.strip():
            console.print("✗ Error: Task title cannot be empty", style="red")
            raise typer.Exit(code=1)

        task = todo_service.add_task(title, description)
        console.print(f"✓ Task '{task.title}' added with ID {task.id}")
    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        raise typer.Exit(code=1)


@app.command("list")
def list_tasks():
    """View all tasks"""
    try:
        tasks = todo_service.list_tasks()
        display_tasks(tasks)
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)


@app.command()
def complete(id: int):
    """Mark task as completed"""
    try:
        if id <= 0:
            console.print(f"✗ Error: Task ID must be positive, got: {id}", style="red")
            raise typer.Exit(code=1)

        success = todo_service.mark_complete(id)
        if success:
            console.print(f"✓ Task {id} marked as complete")
    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        raise typer.Exit(code=1)


@app.command()
def uncomplete(id: int):
    """Mark task as incomplete"""
    try:
        if id <= 0:
            console.print(f"✗ Error: Task ID must be positive, got: {id}", style="red")
            raise typer.Exit(code=1)

        success = todo_service.mark_incomplete(id)
        if success:
            console.print(f"✓ Task {id} marked as incomplete")
    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        raise typer.Exit(code=1)


@app.command()
def update(id: int, title: Optional[str] = None, description: Optional[str] = None):
    """Update task details"""
    try:
        if id <= 0:
            console.print(f"✗ Error: Task ID must be positive, got: {id}", style="red")
            raise typer.Exit(code=1)

        task = todo_service.update_task(id, title, description)
        if task:
            console.print(f"✓ Task {id} updated")
    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        raise typer.Exit(code=1)


@app.command()
def delete(id: int):
    """Delete a task"""
    try:
        if id <= 0:
            console.print(f"✗ Error: Task ID must be positive, got: {id}", style="red")
            raise typer.Exit(code=1)

        success = todo_service.delete_task(id)
        if success:
            console.print(f"✓ Task {id} deleted")
    except ValueError as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Unexpected error: {e}", style="red")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()