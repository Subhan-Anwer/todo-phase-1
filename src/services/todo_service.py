from typing import Dict, List, Optional
from ..models.task import Task


class TodoService:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with unique ID"""
        # Validate title
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        if len(title) > 1000:
            raise ValueError("Task title is too long (maximum 1000 characters)")

        task = Task(
            id=self._next_id,
            title=title.strip(),
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
        if task_id <= 0:
            raise ValueError(f"Task ID must be positive, got: {task_id}")

        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title) > 1000:
                raise ValueError("Task title is too long (maximum 1000 characters)")
            task.title = title.strip()

        if description is not None:
            if description and len(description) > 5000:
                raise ValueError("Task description is too long (maximum 5000 characters)")
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id <= 0:
            raise ValueError(f"Task ID must be positive, got: {task_id}")

        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} does not exist")

        del self._tasks[task_id]
        return True

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as completed"""
        if task_id <= 0:
            raise ValueError(f"Task ID must be positive, got: {task_id}")

        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task.completed = True
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark task as incomplete"""
        if task_id <= 0:
            raise ValueError(f"Task ID must be positive, got: {task_id}")

        task = self._tasks.get(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} does not exist")

        task.completed = False
        return True