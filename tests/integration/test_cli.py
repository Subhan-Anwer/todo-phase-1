import subprocess
import sys
from pathlib import Path


def test_cli_add_task():
    """Integration test for adding a task via CLI"""
    # Test adding a task
    result = subprocess.run([
        sys.executable, "-m", "src", "add", "Integration test task"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)

    assert result.returncode == 0
    assert "✓ Task 'Integration test task' added with ID" in result.stdout


def test_cli_list_empty_tasks():
    """Integration test for listing when there are no tasks"""
    result = subprocess.run([
        sys.executable, "-m", "src", "list"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)

    assert result.returncode == 0
    assert "→ No tasks found" in result.stdout


def test_cli_complete_nonexistent_task():
    """Integration test for completing a non-existent task"""
    result = subprocess.run([
        sys.executable, "-m", "src", "complete", "999"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)

    assert result.returncode == 1
    assert "✗ Error: Task with ID 999 does not exist" in result.stdout or "✗ Error:" in result.stdout


def test_cli_error_handling_for_invalid_args():
    """Integration test for CLI error handling with invalid argument types"""
    # Test with string instead of number for ID
    result = subprocess.run([
        sys.executable, "-m", "src", "complete", "abc"
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)

    # This should fail with argument parsing error
    assert result.returncode != 0


def test_cli_empty_title_error():
    """Integration test for empty title error handling"""
    result = subprocess.run([
        sys.executable, "-m", "src", "add", ""
    ], capture_output=True, text=True, cwd=Path(__file__).parent.parent.parent)

    assert result.returncode == 1
    assert "✗ Error: Task title cannot be empty" in result.stdout