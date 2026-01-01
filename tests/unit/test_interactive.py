"""Unit tests for interactive menu system."""

import pytest
from unittest.mock import patch, MagicMock
from src.cli.menu import InteractiveSession


def test_interactive_session_initialization():
    """Test that InteractiveSession initializes with correct default values."""
    session = InteractiveSession()

    assert session.menu_options == [
        "Add Task",
        "List Tasks",
        "Complete Task",
        "Update Task",
        "Delete Task",
        "Quit"
    ]
    assert session.current_screen == "main_menu"
    assert session.user_selection is None


def test_interactive_session_navigation():
    """Test navigation between screens."""
    session = InteractiveSession()

    # Test initial state
    assert session.current_screen == "main_menu"

    # Test navigation to different screens
    session.navigate("add_task")
    assert session.current_screen == "add_task"

    session.navigate("list_tasks")
    assert session.current_screen == "list_tasks"

    # Test return to main
    session.return_to_main()
    assert session.current_screen == "main_menu"


def test_interactive_session_selection():
    """Test user selection handling."""
    session = InteractiveSession()

    # Initially no selection
    assert session.get_selection() is None

    # Simulate making a selection
    session.user_selection = "Add Task"
    assert session.get_selection() == "Add Task"

    # Change selection
    session.user_selection = "List Tasks"
    assert session.get_selection() == "List Tasks"


def test_interactive_session_show_menu_with_mock():
    """Test show_menu method with mocked terminal menu."""
    session = InteractiveSession()

    # Mock the terminal menu to return a specific selection
    with patch('src.cli.menu.TerminalMenu') as mock_menu:
        mock_instance = MagicMock()
        mock_instance.show.return_value = 0  # "Add Task" option
        mock_menu.return_value = mock_instance

        selection = session.show_menu()

        # The method should return the selected option from menu_options
        # Since index 0 corresponds to "Add Task"
        assert selection == "Add Task"
        assert session.user_selection == "Add Task"


def test_interactive_session_quit_selection():
    """Test that Quit option is properly handled."""
    session = InteractiveSession()

    with patch('src.cli.menu.TerminalMenu') as mock_menu:
        mock_instance = MagicMock()
        mock_instance.show.return_value = 5  # "Quit" option (index 5)
        mock_menu.return_value = mock_instance

        selection = session.show_menu()

        assert selection == "Quit"
        assert session.user_selection == "Quit"


def test_interactive_session_show_menu_cancelled():
    """Test that cancelled selection (None) is handled properly."""
    session = InteractiveSession()

    with patch('src.cli.menu.TerminalMenu') as mock_menu:
        mock_instance = MagicMock()
        mock_instance.show.return_value = None  # User cancelled
        mock_menu.return_value = mock_instance

        selection = session.show_menu()

        assert selection is None
        assert session.user_selection is None


def test_add_task_interactive_with_mock_input():
    """Test the interactive add task function with mocked input."""
    from unittest.mock import patch
    from src.cli.interactive import add_task_interactive
    from src.services.todo_service import TodoService

    # Mock user inputs
    with patch('src.cli.interactive.console.input') as mock_input, \
         patch('src.cli.interactive.console.print') as mock_print:

        mock_input.side_effect = ['Test Task Title', 'Test Description']

        # Call the function
        add_task_interactive()

        # Check that the task was added to the service
        # We can't easily test the service state here, so we'll test the input calls
        assert mock_input.call_count == 2
        mock_input.assert_any_call("Enter task title: ")
        mock_input.assert_any_call("Enter task description (optional, press Enter to skip): ")


def test_add_task_interactive_empty_title():
    """Test the interactive add task function with empty title."""
    from unittest.mock import patch
    from src.cli.interactive import add_task_interactive

    with patch('src.cli.interactive.console.input', return_value=''), \
         patch('src.cli.interactive.console.print') as mock_print:

        add_task_interactive()

        # Verify error message was printed
        mock_print.assert_called()
        # Check that an error message was printed
        error_calls = [call for call in mock_print.call_args_list if '✗ Error:' in str(call)]
        assert len(error_calls) > 0


def test_list_tasks_interactive_with_tasks():
    """Test the interactive list tasks function when there are tasks."""
    from unittest.mock import patch
    from src.cli.interactive import list_tasks_interactive
    from src.services.todo_service import TodoService

    # Create a test service with a task
    service = TodoService()
    service.add_task("Test Task", "Test Description")

    # Mock the service to return our test task
    with patch('src.cli.interactive.todo_service', service), \
         patch('src.cli.interactive.console.print') as mock_print:

        list_tasks_interactive()

        # Verify that the task was displayed
        # Check that print was called (at least once for the table)
        assert mock_print.call_count >= 1


def test_list_tasks_interactive_empty():
    """Test the interactive list tasks function when there are no tasks."""
    from unittest.mock import patch
    from src.cli.interactive import list_tasks_interactive

    # Mock the service to return no tasks
    with patch('src.cli.interactive.todo_service.list_tasks', return_value=[]), \
         patch('src.cli.interactive.console.print') as mock_print:

        list_tasks_interactive()

        # Verify "No tasks found" message was printed
        mock_print.assert_called()
        # Check that the "→ No tasks found" message was printed by looking at all calls
        all_calls_str = str(mock_print.call_args_list)
        assert '→ No tasks found' in all_calls_str


def test_complete_task_interactive_with_tasks():
    """Test the interactive complete task function when there are tasks."""
    from unittest.mock import patch, MagicMock
    from src.cli.interactive import complete_task_interactive
    from src.services.todo_service import TodoService

    # Create a test service with an incomplete task
    service = TodoService()
    task = service.add_task("Test Task", "Test Description")

    # Mock the terminal menu to simulate user selection - patch in the simple_term_menu module
    with patch('src.cli.interactive.todo_service', service), \
         patch('simple_term_menu.TerminalMenu') as mock_menu_class, \
         patch('src.cli.interactive.console.print') as mock_print:

        # Create a mock instance of the terminal menu
        mock_menu_instance = MagicMock()
        mock_menu_instance.show.return_value = 0  # Select the first task
        mock_menu_class.return_value = mock_menu_instance

        complete_task_interactive()

        # Verify that the task was marked as complete
        updated_task = service.get_task(task.id)
        assert updated_task is not None
        assert updated_task.completed is True


def test_complete_task_interactive_empty():
    """Test the interactive complete task function when there are no tasks."""
    from unittest.mock import patch
    from src.cli.interactive import complete_task_interactive

    # Mock the service to return no tasks
    with patch('src.cli.interactive.todo_service.list_tasks', return_value=[]), \
         patch('src.cli.interactive.console.print') as mock_print:

        complete_task_interactive()

        # Verify "No tasks available" message was printed
        mock_print.assert_called()
        # Check that the "→ No tasks available to complete" message was printed
        all_calls_str = str(mock_print.call_args_list)
        assert '→ No tasks available to complete' in all_calls_str


def test_update_task_interactive():
    """Test the interactive update task function."""
    from unittest.mock import patch, MagicMock
    from src.cli.interactive import update_task_interactive
    from src.services.todo_service import TodoService

    # Create a test service with a task
    service = TodoService()
    task = service.add_task("Original Task", "Original Description")

    # Mock the terminal menu and console input
    with patch('src.cli.interactive.todo_service', service), \
         patch('simple_term_menu.TerminalMenu') as mock_menu_class, \
         patch('src.cli.interactive.console.input', side_effect=['New Title', 'New Description']), \
         patch('src.cli.interactive.console.print') as mock_print:

        # Configure the mock menu to return the first task (index 0)
        mock_menu_instance = MagicMock()
        mock_menu_instance.show.return_value = 0  # Select the first task
        mock_menu_class.return_value = mock_menu_instance

        update_task_interactive()

        # Verify that the task was updated
        updated_task = service.get_task(task.id)
        assert updated_task is not None
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"


def test_delete_task_interactive():
    """Test the interactive delete task function."""
    from unittest.mock import patch, MagicMock
    from src.cli.interactive import delete_task_interactive
    from src.services.todo_service import TodoService

    # Create a test service with a task
    service = TodoService()
    task = service.add_task("Task to Delete", "Description to Delete")

    # Mock the terminal menu, console input, and user confirmation
    with patch('src.cli.interactive.todo_service', service), \
         patch('simple_term_menu.TerminalMenu') as mock_menu_class, \
         patch('src.cli.interactive.console.input', return_value='y'), \
         patch('src.cli.interactive.console.print') as mock_print:

        # Configure the mock menu to return the first task (index 0)
        mock_menu_instance = MagicMock()
        mock_menu_instance.show.return_value = 0  # Select the first task
        mock_menu_class.return_value = mock_menu_instance

        delete_task_interactive()

        # Verify that the task was deleted
        deleted_task = service.get_task(task.id)
        assert deleted_task is None