"""Main CLI entry point for the Todo Console Application.

This module provides the command-line interface for managing tasks.
"""

import sys
from typing import Optional

from src.services.task_service import (
    TaskService,
    TaskNotFoundError,
    InvalidTaskInputError,
)


# ANSI Color Codes
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"


def colored(text: str, color: str) -> str:
    """Apply color to text.

    Args:
        text: The text to color.
        color: ANSI color code.

    Returns:
        Colored text string.
    """
    return f"{color}{text}{Colors.RESET}"


def format_task(task: tuple[int, str, str, bool]) -> str:
    """Format a task for display.

    Args:
        task: A tuple of (id, title, description, completed).

    Returns:
        A formatted string representation of the task.
    """
    task_id, title, description, completed = task
    status = colored("[X]", Colors.GREEN) if completed else colored("[ ]", Colors.YELLOW)
    title_colored = colored(title, Colors.BLUE)
    desc = description if description else ""
    return f"{task_id:2} | {status}     | {title_colored:<20} | {desc}"


def parse_task_data(task: tuple[int, str, str, bool]) -> tuple[int, str, str, bool]:
    """Parse task data from storage tuple format.

    Args:
        task: A tuple of (id, title, description, completed).

    Returns:
        The same tuple, ensuring proper types.
    """
    return task


def display_menu() -> None:
    """Display the main menu."""
    print(f"\n{colored('=== Welcome To Todo CLI Menu ===', Colors.YELLOW + Colors.BOLD)}")
    print(f"\n{colored('=== Select your action by entering the number ===', Colors.GREEN + Colors.BOLD)}")
    print(f"\n{colored('1.', Colors.CYAN)} {colored('add', Colors.BLUE)} {colored('<title>', Colors.WHITE)} {colored('[<description>]', Colors.MAGENTA)}")
    print(f"{colored('2.', Colors.CYAN)} {colored('update', Colors.BLUE)} {colored('<id>', Colors.WHITE)} {colored('<title>', Colors.WHITE)} {colored('[<description>]', Colors.MAGENTA)}")
    print(f"{colored('3.', Colors.CYAN)} {colored('delete', Colors.BLUE)} {colored('<id>', Colors.WHITE)}")
    print(f"{colored('4.', Colors.CYAN)} {colored('complete', Colors.BLUE)} {colored('<id>', Colors.WHITE)}")
    print(f"{colored('5.', Colors.CYAN)} {colored('view', Colors.BLUE)}")
    print(f"{colored('6.', Colors.CYAN)} {colored('exit', Colors.RED)}")


def display_tasks(tasks: list[tuple[int, str, str, bool]]) -> None:
    """Display all tasks in a formatted table.

    Args:
        tasks: List of task tuples (id, title, description, completed).
    """
    if not tasks:
        print(colored("\nNo tasks to show.", Colors.YELLOW))
        return

    print(f"\n{colored('ID', Colors.CYAN + Colors.BOLD):2} | {colored('Status', Colors.CYAN + Colors.BOLD):5} | {colored('Title', Colors.CYAN + Colors.BOLD):20} | {colored('Description', Colors.CYAN + Colors.BOLD)}")
    print(f"{colored('-' * 60, Colors.MAGENTA)}")
    for task in tasks:
        print(format_task(task))


def parse_add_command(input_str: str) -> Optional[tuple[str, str]]:
    """Parse the add command.

    Args:
        input_str: The raw input string.

    Returns:
        Tuple of (title, description) or None if invalid.
    """
    # Remove the command prefix
    if not input_str.startswith("add "):
        return None

    args = input_str[4:].strip()
    if not args:
        return None

    # Parse title and optional description
    # Handle quoted strings or simple space-separated
    if args.startswith('"') and '"' in args[1:]:
        # Quoted title
        end_quote = args.find('"', 1)
        title = args[1:end_quote]
        remaining = args[end_quote + 1:].strip()
        description = remaining.strip('"').strip() if remaining else ""
    elif args.startswith("'") and "'" in args[1:]:
        # Single-quoted title
        end_quote = args.find("'", 1)
        title = args[1:end_quote]
        remaining = args[end_quote + 1:].strip()
        description = remaining.strip("'").strip() if remaining else ""
    else:
        # Simple space-separated
        parts = args.split(" ", 1)
        title = parts[0]
        description = parts[1].strip() if len(parts) > 1 else ""

    return (title, description)


def parse_id_command(input_str: str, command: str) -> Optional[int]:
    """Parse a command that takes just an ID.

    Args:
        input_str: The raw input string.
        command: The command prefix (e.g., "delete ", "complete ").

    Returns:
        The task ID as an integer, or None if invalid.
    """
    if not input_str.startswith(command):
        return None

    id_str = input_str[len(command):].strip()
    try:
        return int(id_str)
    except ValueError:
        return None


def parse_update_command(input_str: str) -> Optional[tuple[int, str, str]]:
    """Parse the update command.

    Args:
        input_str: The raw input string.

    Returns:
        Tuple of (id, title, description) or None if invalid.
    """
    if not input_str.startswith("update "):
        return None

    args = input_str[7:].strip()
    if not args:
        return None

    parts = args.split(" ", 2)
    if len(parts) < 2:
        return None

    try:
        task_id = int(parts[0])
    except ValueError:
        return None

    title = parts[1]
    description = parts[2].strip() if len(parts) > 2 else ""

    return (task_id, title, description)


def run_cli() -> None:
    """Run the main CLI loop."""
    task_service = TaskService()

    while True:
        display_menu()
        try:
            choice = input(colored("\n> ", Colors.CYAN + Colors.BOLD)).strip()
        except (EOFError, KeyboardInterrupt):
            print(colored("\nGoodbye!", Colors.CYAN))
            sys.exit(0)

        if choice == "exit" or choice.lower() == "6":
            print(colored("Goodbye!", Colors.CYAN))
            sys.exit(0)

        elif choice == "1" or choice.lower() == "add":
            # Handle add command - may need to prompt for arguments
            if not choice.lower().startswith("add "):
                title = input(colored("Enter task title: ", Colors.YELLOW)).strip()
                if not title:
                    print(colored("Error: Title cannot be empty", Colors.RED))
                    continue
                description = input(colored("Enter task description (optional): ", Colors.YELLOW)).strip()
                try:
                    task = task_service.create_task(title, description)
                    print(colored(f"Task added with ID {task.id}", Colors.GREEN))
                except InvalidTaskInputError as e:
                    print(colored(f"Error: {e}", Colors.RED))
            else:
                result = parse_add_command(choice)
                if result is None:
                    print(colored("Error: Invalid add command. Usage: add <title> [<description>]", Colors.RED))
                    continue

                title, description = result
                try:
                    task = task_service.create_task(title, description)
                    print(colored(f"Task added with ID {task.id}", Colors.GREEN))
                except InvalidTaskInputError as e:
                    print(colored(f"Error: {e}", Colors.RED))

        elif choice == "2" or choice.lower().startswith("update"):
            # Handle update command
            if not choice.lower().startswith("update "):
                task_id_str = input(colored("Enter task ID: ", Colors.YELLOW)).strip()
                try:
                    task_id = int(task_id_str)
                except ValueError:
                    print(colored("Error: Invalid task ID", Colors.RED))
                    continue
                title = input(colored("Enter new title: ", Colors.YELLOW)).strip()
                if not title:
                    print(colored("Error: Title cannot be empty", Colors.RED))
                    continue
                description = input(colored("Enter new description (optional): ", Colors.YELLOW)).strip()
                try:
                    task = task_service.update_task(task_id, title, description)
                    print(colored(f"Task {task.id} updated", Colors.GREEN))
                except TaskNotFoundError:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))
                except InvalidTaskInputError as e:
                    print(colored(f"Error: {e}", Colors.RED))
            else:
                result = parse_update_command(choice)
                if result is None:
                    print(colored("Error: Invalid update command. Usage: update <id> <title> [<description>]", Colors.RED))
                    continue

                task_id, title, description = result
                try:
                    task = task_service.update_task(task_id, title, description)
                    print(colored(f"Task {task.id} updated", Colors.GREEN))
                except TaskNotFoundError:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))
                except InvalidTaskInputError as e:
                    print(colored(f"Error: {e}", Colors.RED))

        elif choice == "3" or choice.lower().startswith("delete"):
            # Handle delete command
            if not choice.lower().startswith("delete "):
                task_id_str = input(colored("Enter task ID to delete: ", Colors.YELLOW)).strip()
                try:
                    task_id = int(task_id_str)
                except ValueError:
                    print(colored("Error: Invalid task ID", Colors.RED))
                    continue
                if task_service.delete_task(task_id):
                    print(colored(f"Task {task_id} deleted", Colors.GREEN))
                else:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))
            else:
                task_id = parse_id_command(choice, "delete ")
                if task_id is None:
                    print(colored("Error: Invalid delete command. Usage: delete <id>", Colors.RED))
                    continue

                if task_service.delete_task(task_id):
                    print(colored(f"Task {task_id} deleted", Colors.GREEN))
                else:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))

        elif choice == "4" or choice.lower().startswith("complete"):
            # Handle complete command
            if not choice.lower().startswith("complete "):
                task_id_str = input(colored("Enter task ID to complete: ", Colors.YELLOW)).strip()
                try:
                    task_id = int(task_id_str)
                except ValueError:
                    print(colored("Error: Invalid task ID", Colors.RED))
                    continue
                task = task_service.toggle_complete(task_id)
                if task is None:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))
                elif task.completed:
                    print(colored(f"Task {task.id} marked complete", Colors.GREEN))
                else:
                    print(colored(f"Task {task.id} marked incomplete", Colors.YELLOW))
            else:
                task_id = parse_id_command(choice, "complete ")
                if task_id is None:
                    print(colored("Error: Invalid complete command. Usage: complete <id>", Colors.RED))
                    continue

                task = task_service.toggle_complete(task_id)
                if task is None:
                    print(colored(f"Error: Task with ID {task_id} not found", Colors.RED))
                elif task.completed:
                    print(colored(f"Task {task.id} marked complete", Colors.GREEN))
                else:
                    print(colored(f"Task {task.id} marked incomplete", Colors.YELLOW))

        elif choice == "5" or choice.lower() == "view":
            tasks = task_service.get_all_tasks()
            # Convert Task objects to tuples for display
            task_tuples = [
                (t.id, t.title, t.description, t.completed)
                for t in tasks
            ]
            display_tasks(task_tuples)

        else:
            print(colored("Error: Invalid command. Please select from the menu.", Colors.RED))


def main() -> None:
    """Entry point for the application."""
    run_cli()


if __name__ == "__main__":
    main()
