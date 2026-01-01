# Data Model: Phase II Full-Stack Todo Application

**Date**: 2025-12-25 | **Feature**: Phase II Full-Stack Todo App

---

## Entities

### User

**Description**: Authenticated user with personal task collection.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | string (UUID) | PK, unique | Primary identifier |
| `email` | string | unique, not null | User email address |
| `name` | string | nullable | Display name |
| `image` | string | nullable | Avatar URL |
| `created_at` | timestamp | not null | Account creation time |
| `updated_at` | timestamp | not null | Last profile update |

**Relationships**:
- One-to-many with `Task` (user's tasks)
- Cascade delete: deleting user deletes all tasks

---

### Task

**Description**: Individual todo item belonging to a user.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | integer | PK, auto-increment | Task identifier |
| `user_id` | string | FK → users.id, not null | Owner reference |
| `title` | string | not null, max 200 | Task title |
| `description` | string | max 1000 | Optional details |
| `completed` | boolean | default false | Completion status |
| `created_at` | timestamp | not null | Creation time |
| `updated_at` | timestamp | not null | Last modification |

**Relationships**:
- Many-to-one with `User` (owned by exactly one user)
- No cascade from task to user

---

## Entity Relationship Diagram

```
┌─────────┐         ┌─────────┐
│  users  │ 1    *  │  tasks  │
│─────────│─────────│─────────│
│ id (PK) │◄─────── │ user_id │
│ email   │         │ id (PK) │
│ ...     │         │ title   │
└─────────┘         │ ...     │
                    └─────────┘
```

---

## SQLModel Definitions

```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .task import Task

class User(SQLModel, table=True):
    """User entity for authentication and task ownership."""
    
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    email: str = Field(unique=True, index=True, max_length=255)
    name: str | None = Field(default=None, max_length=255)
    image: str | None = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: list["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

```python
# backend/app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Task(SQLModel, table=True):
    """Task entity representing a todo item."""
    
    id: int | None = Field(default=None, primary_key=True, autogen=True)
    user_id: str = Field(
        foreign_key="user.id",
        on_delete="CASCADE",
        index=True
    )
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="tasks")
```

---

## API Schemas (Pydantic)

```python
# backend/app/schemas/task.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    """Schema for creating a task."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskResponse(BaseModel):
    """Schema for task API responses."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

---

## Validation Rules

| Operation | Rule |
|-----------|------|
| Create task | title required (1-200 chars), description optional (0-1000 chars) |
| Update task | At least one field (title or description) required |
| List tasks | Filtered by authenticated user's ID |
| Delete task | Only owner can delete; cascade handles cleanup |

---

**Data model finalized**: 2025-12-25
