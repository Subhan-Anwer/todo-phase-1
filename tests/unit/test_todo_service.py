import pytest
from src.models.task import Task
from src.services.todo_service import TodoService


def test_add_task_basic():
    """Test adding a basic task"""
    service = TodoService()
    task = service.add_task("Test task")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.completed == False
    assert task.description is None


def test_add_task_with_description():
    """Test adding a task with description"""
    service = TodoService()
    task = service.add_task("Test task", "A description")

    assert task.id == 1
    assert task.title == "Test task"
    assert task.description == "A description"


def test_add_task_validation():
    """Test task validation"""
    service = TodoService()

    # Test empty title
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.add_task("")

    # Test whitespace-only title
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.add_task("   ")

    # Test long title
    with pytest.raises(ValueError, match="Task title is too long"):
        service.add_task("a" * 1001)


def test_get_task():
    """Test getting a specific task"""
    service = TodoService()
    added_task = service.add_task("Test task")

    retrieved_task = service.get_task(added_task.id)
    assert retrieved_task is not None
    assert retrieved_task.id == added_task.id
    assert retrieved_task.title == added_task.title


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    service = TodoService()
    task = service.get_task(999)
    assert task is None


def test_list_tasks():
    """Test listing all tasks"""
    service = TodoService()
    service.add_task("Task 1")
    service.add_task("Task 2")

    tasks = service.list_tasks()
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_update_task():
    """Test updating task details"""
    service = TodoService()
    original_task = service.add_task("Original title", "Original description")

    updated_task = service.update_task(original_task.id, "New title", "New description")

    assert updated_task.title == "New title"
    assert updated_task.description == "New description"


def test_update_task_validation():
    """Test validation during task updates"""
    service = TodoService()
    task = service.add_task("Original title")

    # Test empty title during update
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        service.update_task(task.id, "")


def test_update_nonexistent_task():
    """Test updating a task that doesn't exist"""
    service = TodoService()

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.update_task(999, "New title")


def test_delete_task():
    """Test deleting a task"""
    service = TodoService()
    task = service.add_task("Test task")

    result = service.delete_task(task.id)
    assert result is True

    # Verify task is gone
    assert service.get_task(task.id) is None


def test_delete_nonexistent_task():
    """Test deleting a task that doesn't exist"""
    service = TodoService()

    with pytest.raises(ValueError, match="Task with ID 999 does not exist"):
        service.delete_task(999)


def test_mark_complete():
    """Test marking a task as complete"""
    service = TodoService()
    task = service.add_task("Test task")

    # Initially incomplete
    assert task.completed == False

    # Mark as complete
    result = service.mark_complete(task.id)
    assert result is True

    # Verify it's now complete
    updated_task = service.get_task(task.id)
    assert updated_task.completed == True


def test_mark_incomplete():
    """Test marking a task as incomplete"""
    service = TodoService()
    task = service.add_task("Test task")

    # Mark as complete first
    service.mark_complete(task.id)
    assert service.get_task(task.id).completed == True

    # Mark as incomplete
    result = service.mark_incomplete(task.id)
    assert result is True

    # Verify it's now incomplete
    updated_task = service.get_task(task.id)
    assert updated_task.completed == False


def test_service_id_sequencing():
    """Test that task IDs are properly sequenced"""
    service = TodoService()
    task1 = service.add_task("Task 1")
    task2 = service.add_task("Task 2")
    task3 = service.add_task("Task 3")

    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3