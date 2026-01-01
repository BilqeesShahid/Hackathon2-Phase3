"""Task model for SQLModel."""
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, ForeignKey
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User


class Task(SQLModel, table=True):
    """Task entity representing a todo item."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(
        sa_column=Column(String, ForeignKey("user.id", ondelete="CASCADE"), index=True)
    )
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")
