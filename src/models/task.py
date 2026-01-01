"""Task data model for the Todo Console Application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: A unique identifier assigned at creation.
        title: A required string describing the task.
        description: An optional string with additional details.
        completed: A boolean indicating task status (False = incomplete, True = complete).
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False
