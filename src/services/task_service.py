"""Task service for managing todo tasks in memory.

This module provides the TaskService class which handles all CRUD operations
for tasks stored in memory.
"""

from typing import Optional

from src.models.task import Task


class TaskServiceError(Exception):
    """Base exception for TaskService errors."""
    pass


class TaskNotFoundError(TaskServiceError):
    """Raised when a task ID is not found."""
    pass


class InvalidTaskInputError(TaskServiceError):
    """Raised when task input validation fails."""
    pass


class TaskService:
    """Service for managing tasks in memory.

    Attributes:
        _tasks: Internal list storing all tasks.
        _next_id: Counter for generating unique task IDs.
    """

    def __init__(self) -> None:
        """Initialize the TaskService with empty storage."""
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """Create a new task with a unique ID and incomplete status.

        Args:
            title: The task title (required, non-empty).
            description: Optional task description.

        Returns:
            The newly created Task.

        Raises:
            InvalidTaskInputError: If title is empty or whitespace.
        """
        if not title or not title.strip():
            raise InvalidTaskInputError("Task title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description.strip() if description else "",
            completed=False
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks ordered by ID.

        Returns:
            A list of all tasks in ID order.
        """
        return list(self._tasks)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self, task_id: int, title: str, description: str = ""
    ) -> Task:
        """Update an existing task's title and description.

        Args:
            task_id: The ID of the task to update.
            title: The new task title (required, non-empty).
            description: The new task description.

        Returns:
            The updated Task.

        Raises:
            TaskNotFoundError: If task_id is not found.
            InvalidTaskInputError: If title is empty or whitespace.
        """
        if not title or not title.strip():
            raise InvalidTaskInputError("Task title cannot be empty")

        task = self.get_task_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        task.title = title.strip()
        task.description = description.strip() if description else ""
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if not found.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated Task if found, None otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task is not None:
            task.completed = not task.completed
        return task
