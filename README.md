# Console To-Do Application

A command-line interface (CLI) application for managing todo tasks. This application allows users to create, view, update, complete, and delete tasks directly from the terminal.

## Prerequisites

- Python 3.12 or higher
- UV package manager

## Installation

1. Clone or download the project
2. Navigate to the project directory
3. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

All commands should be run using `uv run` to ensure the proper environment is used:

### Interactive Mode (New!)
Launch the interactive menu system by running without any arguments:
```bash
uv run python -m src
```
This will launch an arrow-key navigable menu system where you can:
- Use UP/DOWN arrow keys to navigate menu options
- Press ENTER to select an option
- Menu includes: Add Task, List Tasks, Complete Task, Update Task, Delete Task, Quit

### Command-Line Mode (Backward Compatible)
The existing command-line functionality remains unchanged:

#### Add a Task
```bash
uv run python -m src add "Task title" "Optional description"
```

#### View All Tasks
```bash
uv run python -m src list
```

#### Complete a Task
```bash
uv run python -m src complete 1
```

#### Mark a Task as Incomplete
```bash
uv run python -m src uncomplete 1
```

#### Update Task Details
```bash
uv run python -m src update 1 "New title" "Optional new description"
```

#### Delete a Task
```bash
uv run python -m src delete 1
```

#### Get Help
```bash
uv run python -m src --help
```

## Features

1. **Add Task**: Create new tasks with unique IDs
2. **View Tasks**: List all tasks with status
3. **Complete/Uncomplete**: Toggle task completion status
4. **Update Task**: Modify task details
5. **Delete Task**: Remove tasks from the list
6. **Error Handling**: Graceful handling of invalid inputs
7. **User Feedback**: Clear messages for all operations

## Project Structure

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
└── pyproject.toml
```

## Testing

Run all tests:
```bash
pytest
```

Run unit tests:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```

## Error Handling

The application follows these error handling principles:
- The application will never crash due to user input
- All errors provide clear feedback using the format: `✗ Error: <message>`
- Success messages use the format: `✓ <message>`
- Informational messages use the format: `→ <message>`