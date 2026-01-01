"""Menu navigation and selection logic for interactive mode."""

from typing import List, Optional
from simple_term_menu import TerminalMenu
from rich.console import Console

console = Console()


class InteractiveSession:
    """Represents a single run of the interactive mode with menu navigation and operation flow."""

    def __init__(self):
        self.menu_options = [
            "Add Task",
            "List Tasks",
            "Complete Task",
            "Update Task",
            "Delete Task",
            "Quit"
        ]
        self.current_screen = "main_menu"
        self.user_selection: Optional[str] = None

    def show_menu(self) -> Optional[str]:
        """Display menu options with arrow-key navigation."""
        try:
            terminal_menu = TerminalMenu(
                self.menu_options,
                title="Select an option:",
                menu_cursor="> ",
                menu_cursor_style=("fg_red", "bold"),
                menu_highlight_style=("bg_red", "fg_yellow"),
                cycle_cursor=True,
                clear_screen=False,
            )
            menu_entry_index = terminal_menu.show()

            if menu_entry_index is not None:
                self.user_selection = self.menu_options[menu_entry_index]
                return self.user_selection
            return None
        except KeyboardInterrupt:
            console.print("\n[X] Operation cancelled by user.")
            return "Quit"

    def get_selection(self) -> Optional[str]:
        """Capture user's menu selection."""
        return self.user_selection

    def navigate(self, screen: str) -> None:
        """Move between different interactive screens."""
        self.current_screen = screen

    def return_to_main(self) -> None:
        """Return to main menu after operation completion."""
        self.current_screen = "main_menu"