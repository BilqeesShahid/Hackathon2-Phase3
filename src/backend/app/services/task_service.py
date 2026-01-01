"""Task service for Phase II Todo Application."""
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.models.task import Task


class TaskService:
    """Service class for task CRUD operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user_id: str, title: str, description: Optional[str] = None) -> Task:
        """Create a new task for a user."""
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_by_user(self, user_id: str) -> List[Task]:
        """Get all tasks for a user."""
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
        )
        return list(self.session.exec(statement).all())

    def get_by_id(self, task_id: int, user_id: str) -> Optional[Task]:
        """Get a specific task by ID, ensuring user ownership."""
        statement = (
            select(Task)
            .where(Task.id == task_id)
            .where(Task.user_id == user_id)
        )
        return self.session.exec(statement).first()

    def update(
        self,
        task_id: int,
        user_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Optional[Task]:
        """Update a task, ensuring user ownership."""
        task = self.get_by_id(task_id, user_id)
        if not task:
            return None

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task_id: int, user_id: str) -> bool:
        """Delete a task, ensuring user ownership."""
        task = self.get_by_id(task_id, user_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_complete(self, task_id: int, user_id: str) -> Optional[Task]:
        """Toggle task completion status."""
        task = self.get_by_id(task_id, user_id)
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        self.session.commit()
        self.session.refresh(task)
        return task
