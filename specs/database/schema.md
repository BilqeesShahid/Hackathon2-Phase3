# Database Schema — Phase II

## Database
**Neon Serverless PostgreSQL**

## Tables

### users
Managed by Better Auth

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | string | Primary Key |
| `email` | string | Unique, Not Null |
| `name` | string | nullable |
| `image` | string | nullable |
| `created_at` | timestamp | Not Null |
| `updated_at` | timestamp | Not Null |

---

### tasks

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | integer | Primary Key, Auto-increment |
| `user_id` | string | Foreign Key → users.id, Not Null |
| `title` | string | Not Null, Max 200 chars |
| `description` | text | Max 1000 chars |
| `completed` | boolean | Default false, Not Null |
| `created_at` | timestamp | Not Null |
| `updated_at` | timestamp | Not Null |

---

## Constraints

### Foreign Key
- `tasks.user_id` → `users.id`
- ON DELETE CASCADE (deleting user deletes all their tasks)

### Indexes
- `idx_tasks_user_id` - For efficient user-scoped queries
- `idx_tasks_completed` - For filtering by completion status

---

## SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    image: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, autogen=True)
    user_id: str = Field(foreign_key="user.id", on_delete="CASCADE")
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="tasks")
```

---

**Last Updated**: 2025-12-25
