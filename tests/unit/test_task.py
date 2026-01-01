import pytest
from src.models.task import Task
from src.services.todo_service import TodoService


def test_task_creation():
    """Test basic task creation"""
    task = Task(id=1, title="Test task", completed=False)
    assert task.id == 1
    assert task.title == "Test task"
    assert task.completed == False
    assert task.description is None


def test_task_with_description():
    """Test task creation with description"""
    task = Task(id=1, title="Test task", description="A description", completed=False)
    assert task.description == "A description"


def test_task_default_values():
    """Test task default values"""
    task = Task(id=1, title="Test task")
    assert task.completed == False
    assert task.description is None