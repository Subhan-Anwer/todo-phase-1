# Data Model: Interactive CLI To-Do Application

## Entity: Task
*Inherited from existing application - no changes needed*

### Fields
- **id** (int, required, unique)
  - Auto-generated unique identifier for each task
  - Sequential numbering starting from 1
  - Primary key for task identification

- **title** (str, required)
  - The main description of the task
  - Cannot be empty or null
  - Minimum length: 1 character
  - Maximum length: 1000 characters (for practicality)

- **description** (str, optional)
  - Additional details about the task
  - Can be null or empty
  - Maximum length: 5000 characters (for practicality)

- **completed** (bool, required)
  - Status indicating whether the task is completed
  - Default value: False (incomplete by default when creating)
  - Can be toggled between True (completed) and False (incomplete)

### Validation Rules
1. **Title Validation**:
   - Cannot be empty or contain only whitespace
   - Must be at least 1 non-whitespace character
   - Maximum 1000 characters

2. **ID Validation**:
   - Must be a positive integer (>= 1)
   - Must be unique within the task collection
   - Auto-incremented when new tasks are created

3. **Description Validation**:
   - Optional field, can be null
   - If provided, maximum 5000 characters

4. **Completion Status Validation**:
   - Must be boolean value (True/False)
   - Default False when task is created

### State Transitions
- **Creation**: `completed = False` (default)
- **Completion**: `completed = False` → `completed = True`
- **Reversion**: `completed = True` → `completed = False`

## Entity: InteractiveSession (New)
*Represents a single run of the interactive mode*

### Fields
- **menu_options** (List[str], required)
  - The available menu options for the current screen
  - Options include: "Add Task", "List Tasks", "Complete Task", "Update Task", "Delete Task", "Quit"

- **current_screen** (str, required)
  - The current display state: "main_menu", "add_task", "list_tasks", "complete_task", "update_task", "delete_task"

- **user_selection** (str, optional)
  - The option selected by the user in the current interaction

### Operations
1. **Show Menu**: Display menu options with arrow-key navigation
2. **Get Selection**: Capture user's menu selection
3. **Navigate**: Move between different interactive screens
4. **Return to Main**: Return to main menu after operation completion

## Entity: TodoList (Collection)
*Inherited from existing application - no changes needed*

### Fields
- **tasks** (Dict[int, Task], required)
  - In-memory collection of Task objects indexed by ID
  - Maintains all tasks in the application
  - Provides O(1) access to tasks by ID

- **next_id** (int, required)
  - Tracks the next available ID for new tasks
  - Auto-incremented when new tasks are added
  - Ensures unique IDs for all tasks

### Operations
1. **Add Task**: Adds a new Task to the collection
2. **Get Task**: Retrieves a Task by its ID
3. **Update Task**: Modifies existing Task properties
4. **Delete Task**: Removes a Task from the collection
5. **List Tasks**: Returns all Tasks in the collection
6. **Mark Complete**: Updates a Task's completion status to True
7. **Mark Incomplete**: Updates a Task's completion status to False

### Constraints
- All data stored in-memory only (no persistence)
- Single-user access (no concurrency concerns)
- Task IDs are never reused after deletion
- Maximum theoretical capacity limited only by available memory

## Relationships
- TodoList contains multiple Task entities
- Each Task belongs to exactly one TodoList
- Task IDs are unique within the TodoList
- InteractiveSession interacts with TodoList through TodoService