import sys
from .cli.app import app
from .cli.interactive import run_interactive_mode, detect_interactive_mode


def main():
    if detect_interactive_mode():
        # No arguments provided - run interactive mode
        run_interactive_mode()
    else:
        # Arguments provided - run command-line mode
        app()


if __name__ == "__main__":
    main()