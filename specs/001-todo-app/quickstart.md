# Quickstart Guide: Console To-Do Application

## Prerequisites

- Python 3.12 or higher
- UV package manager installed

## Setup

1. **Clone or create the project directory**
   ```bash
   mkdir todo-app
   cd todo-app
   ```

2. **Initialize the project with UV**
   ```bash
   uv init
   ```

3. **Install required dependencies**
   ```bash
   uv add typer rich
   ```

## Project Structure

The recommended structure for the todo application:

```
todo-app/
├── src/
│   ├── __main__.py          # Application entry point
│   ├── models/
│   │   └── task.py          # Task data model
│   ├── services/
│   │   └── todo_service.py  # Business logic
│   └── cli/
│       └── app.py           # CLI interface
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

## Basic Implementation

### 1. Task Model (`src/models/task.py`)

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
```

### 2. Todo Service (`src/services/todo_service.py`)

```python
from typing import Dict, List, Optional
from .models.task import Task

class TodoService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with unique ID"""
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task"""
        return self._tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        """Get all tasks"""
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update task details"""
        task = self._tasks.get(task_id)
        if task:
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as completed"""
        task = self._tasks.get(task_id)
        if task:
            task.completed = True
            return True
        return False

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark task as incomplete"""
        task = self._tasks.get(task_id)
        if task:
            task.completed = False
            return True
        return False
```

### 3. CLI Interface (`src/cli/app.py`)

```python
import typer
from typing import Optional
from rich.console import Console
from rich.table import Table

from ..services.todo_service import TodoService
from ..models.task import Task

app = typer.Typer()
console = Console()
todo_service = TodoService()

def display_tasks(tasks: List[Task]) -> None:
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
def add(title: str, description: Optional[str] = None):
    """Add a new task with optional description"""
    try:
        # Validate title
        if not title or not title.strip():
            console.print("✗ Error: Task title cannot be empty", style="red")
            raise typer.Exit(code=1)

        task = todo_service.add_task(title, description)
        console.print(f"✓ Task '{task.title}' added with ID {task.id}")
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)

@app.command("list")
def list_tasks():
    """View all tasks"""
    tasks = todo_service.list_tasks()
    display_tasks(tasks)

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
        else:
            console.print(f"✗ Error: Task with ID {id} does not exist", style="red")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
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
        else:
            console.print(f"✗ Error: Task with ID {id} does not exist", style="red")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
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
        else:
            console.print(f"✗ Error: Task with ID {id} does not exist", style="red")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
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
        else:
            console.print(f"✗ Error: Task with ID {id} does not exist", style="red")
            raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"✗ Error: {e}", style="red")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
```

### 4. Entry Point (`src/__main__.py`)

```python
from .cli.app import app

if __name__ == "__main__":
    app()
```

## Running the Application

1. **Run directly with Python:**
   ```bash
   python -m src
   ```

2. **Run with UV:**
   ```bash
   uv run src
   ```

## Available Commands

- `add`: Add a new task
  ```bash
  python -m src add "Buy groceries" "Milk, eggs, bread"
  ```

- `list`: View all tasks
  ```bash
  python -m src list
  ```

- `complete`: Mark task as completed
  ```bash
  python -m src complete 1
  ```

- `uncomplete`: Mark task as incomplete
  ```bash
  python -m src uncomplete 1
  ```

- `update`: Update task details
  ```bash
  python -m src update 1 "New title" "New description"
  ```

- `delete`: Delete a task
  ```bash
  python -m src delete 1
  ```

## Testing

Create unit tests in the `tests/unit/` directory:

```python
# tests/unit/test_task.py
import pytest
from src.models.task import Task

def test_task_creation():
    task = Task(id=1, title="Test task", completed=False)
    assert task.id == 1
    assert task.title == "Test task"
    assert task.completed == False

def test_task_with_description():
    task = Task(id=1, title="Test task", description="A description", completed=False)
    assert task.description == "A description"
```

## Key Features Implemented

1. **Add Task**: Create new tasks with unique IDs
2. **View Tasks**: List all tasks with status
3. **Complete/Uncomplete**: Toggle task completion status
4. **Update Task**: Modify task details
5. **Delete Task**: Remove tasks from the list
6. **Error Handling**: Graceful handling of invalid inputs
7. **User Feedback**: Clear messages for all operations

This quickstart guide provides everything needed to begin implementing the CLI todo application following the constitutional requirements.