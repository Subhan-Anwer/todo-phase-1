#!/usr/bin/env python3
"""Simple test script for edge case validation."""
import sys
import os

# Add the project root to the path so we can import modules properly
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.abspath(project_root))

from src.services.todo_service import TodoService

def test_invalid_task_operations():
    """Test invalid task operations."""
    service = TodoService()
    try:
        result = service.update_task(999, 'Invalid task')
        print('Should have failed')
    except ValueError as e:
        print('Error caught: ' + str(e))

def test_error_handling():
    """Test error handling for invalid input."""
    service = TodoService()
    try:
        task = service.add_task('')
        print('Should have failed')
    except ValueError as e:
        print('Error caught: ' + str(e))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "invalid_ops":
        test_invalid_task_operations()
    elif len(sys.argv) > 1 and sys.argv[1] == "error_handling":
        test_error_handling()
    else:
        # Default: test no tasks
        service = TodoService()
        tasks = service.list_tasks()
        print('Tasks available: ' + str(len(tasks)))