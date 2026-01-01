# Quickstart Guide: Interactive CLI To-Do Application

## Prerequisites

- Python 3.12 or higher
- UV package manager installed

## Setup

1. **Install the new dependency**
   ```bash
   uv add simple-term-menu
   ```

## Interactive Mode Usage

### Launch Interactive Mode
```bash
uv run python -m src
```
When run without arguments, the application will launch the interactive menu mode.

### Navigate the Interactive Menu
- Use **UP/DOWN arrow keys** to navigate between menu options
- Press **ENTER** to select an option
- The main menu includes: Add Task, List Tasks, Complete Task, Update Task, Delete Task, Quit

### Add a Task (Interactive)
1. Select "Add Task" from the main menu
2. Enter the task title when prompted
3. Optionally enter a task description
4. The task will be created and you'll return to the main menu

### List Tasks (Interactive)
1. Select "List Tasks" from the main menu
2. All tasks will be displayed with ID, status (✓/✗), title, and description
3. Press any key to return to the main menu

### Complete a Task (Interactive)
1. Select "Complete Task" from the main menu
2. Choose a task from the list of incomplete tasks
3. The task will be marked as complete with confirmation
4. Return to the main menu

### Update a Task (Interactive)
1. Select "Update Task" from the main menu
2. Choose a task from the list of all tasks
3. Enter new title and/or description when prompted
4. The task will be updated with confirmation
5. Return to the main menu

### Delete a Task (Interactive)
1. Select "Delete Task" from the main menu
2. Choose a task from the list of all tasks
3. Confirm deletion when prompted
4. The task will be removed with confirmation
5. Return to the main menu

## Command-Line Mode (Backward Compatibility)

The existing command-line functionality remains unchanged:

### Add a Task
```bash
uv run python -m src add "Task title" "Optional description"
```

### View All Tasks
```bash
uv run python -m src list
```

### Complete a Task
```bash
uv run python -m src complete 1
```

### Mark a Task as Incomplete
```bash
uv run python -m src uncomplete 1
```

### Update Task Details
```bash
uv run python -m src update 1 "New title" "New description"
```

### Delete a Task
```bash
uv run python -m src delete 1
```

## Key Features Implemented

1. **Interactive Menu**: Arrow-key navigable menu system
2. **Backward Compatibility**: All existing command-line functions preserved
3. **Consistent UI**: Same feedback format (✓ for success, ✗ for errors, → for info)
4. **Error Handling**: Graceful handling of invalid inputs in both modes
5. **User Experience**: Intuitive navigation and clear prompts

## Implementation Structure

The interactive mode is implemented in:
- `src/cli/interactive.py` - Main interactive menu system
- `src/cli/menu.py` - Menu navigation and selection logic
- `src/__main__.py` - Mode detection (interactive vs command-line)

The interactive mode reuses the existing:
- `src/services/todo_service.py` - Business logic
- `src/models/task.py` - Data model
- `src/cli/app.py` - Command-line interface (unchanged)