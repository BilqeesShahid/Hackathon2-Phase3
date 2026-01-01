# Data Model: AI-Powered Todo Chatbot

**Feature**: 002-ai-chatbot
**Date**: 2025-12-29
**Phase**: Phase 1 — Design & Contracts

---

## Overview

Phase III extends the existing database schema with two new tables to support conversational state management while maintaining strict user isolation and stateless backend requirements.

---

## Existing Schema (Phase II)

### Table: users
**Purpose**: Store authenticated user information

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | String | PRIMARY KEY | Unique user identifier (from Better Auth) |
| email | String | UNIQUE, NOT NULL | User email |
| created_at | Timestamp | NOT NULL | Account creation time |
| updated_at | Timestamp | NOT NULL | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`

---

### Table: tasks
**Purpose**: Store user tasks

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PRIMARY KEY, AUTO INCREMENT | Unique task identifier |
| user_id | String | FOREIGN KEY (users.id), NOT NULL | Task owner |
| title | String | NOT NULL | Task title |
| description | Text | NULL | Task description (optional) |
| completed | Boolean | DEFAULT FALSE | Completion status |
| created_at | Timestamp | NOT NULL | Task creation time |
| updated_at | Timestamp | NOT NULL | Last update time |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for efficient user task queries)
- INDEX on `user_id, completed` (for filtered queries)

**Relationships**:
- `user_id` → `users.id` (CASCADE DELETE)

---

## New Schema (Phase III)

### Table: conversations
**Purpose**: Store conversation metadata for chat sessions

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique conversation identifier |
| user_id | String | FOREIGN KEY (users.id), NOT NULL | Conversation owner |
| created_at | Timestamp | NOT NULL | Conversation start time |
| updated_at | Timestamp | NOT NULL | Last message time |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `user_id` (for retrieving user's conversations)
- INDEX on `user_id, updated_at DESC` (for recent conversations)

**Relationships**:
- `user_id` → `users.id` (CASCADE DELETE)

**Validation Rules**:
- `id` must be valid UUID v4
- `user_id` must exist in `users` table
- `updated_at` must be >= `created_at`

**Lifecycle**:
- **Created**: When user sends first message in new conversation
- **Updated**: `updated_at` refreshed on every new message
- **Deleted**: When user account deleted (CASCADE) or manual cleanup

---

### Table: messages
**Purpose**: Store individual chat messages (user + assistant)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique message identifier |
| conversation_id | UUID | FOREIGN KEY (conversations.id), NOT NULL | Parent conversation |
| role | Enum | NOT NULL | Message sender: "user" or "assistant" |
| content | Text | NOT NULL | Message content |
| created_at | Timestamp | NOT NULL | Message creation time |

**Indexes**:
- PRIMARY KEY on `id`
- INDEX on `conversation_id` (for retrieving conversation history)
- INDEX on `conversation_id, created_at ASC` (for chronological ordering)

**Relationships**:
- `conversation_id` → `conversations.id` (CASCADE DELETE)

**Validation Rules**:
- `conversation_id` must exist in `conversations` table
- `role` must be "user" or "assistant"
- `content` must be non-empty (min length: 1, max length: 10000)

**Lifecycle**:
- **Created**: Immediately when user sends message or agent generates response
- **Updated**: Never (messages are immutable)
- **Deleted**: When conversation deleted (CASCADE) or manual cleanup

---

## Entity Relationships

```
users (1) ──< conversations (N)
users (1) ──< tasks (N)
conversations (1) ──< messages (N)
```

**User Isolation Enforcement**:
- All queries on `conversations` MUST filter by `user_id`
- All queries on `messages` MUST join through `conversations` to validate `user_id`
- Cross-user data access is impossible due to foreign key constraints + query-level filtering

---

## SQLModel Definitions

### Conversation Model

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List

class Conversation(SQLModel, table=True):
    """
    Conversation metadata for chat sessions.

    Relationships:
    - Belongs to one User
    - Has many Messages
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    class Config:
        arbitrary_types_allowed = True
```

---

### Message Model

```python
from sqlmodel import SQLModel, Field, Relationship, Column, Enum as SQLEnum
from sqlalchemy import Text
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4

class MessageRole(str, Enum):
    """Message sender role"""
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    """
    Individual chat message (user or assistant).

    Relationships:
    - Belongs to one Conversation
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(SQLEnum(MessageRole)))
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")

    class Config:
        arbitrary_types_allowed = True
```

---

### Updated User Model

```python
class User(SQLModel, table=True):
    """
    Authenticated user (managed by Better Auth).

    Relationships:
    - Has many Tasks
    - Has many Conversations
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    conversations: List["Conversation"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
```

---

## Database Migration

### Alembic Migration Script

```python
"""Add conversations and messages tables

Revision ID: 002_add_conversations
Revises: 001_initial_schema
Create Date: 2025-12-29
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# revision identifiers
revision = '002_add_conversations'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('ix_conversations_user_updated', 'conversations', ['user_id', 'updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('conversation_id', UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.Enum('user', 'assistant', name='message_role'), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('ix_messages_conversation_created', 'messages', ['conversation_id', 'created_at'])

def downgrade():
    op.drop_index('ix_messages_conversation_created', table_name='messages')
    op.drop_index('ix_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('ix_conversations_user_updated', table_name='conversations')
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')

    op.execute('DROP TYPE message_role')
```

---

## Query Patterns

### Common Queries

#### 1. Create New Conversation
```python
def create_conversation(user_id: str) -> Conversation:
    """Create a new conversation for user"""
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

#### 2. Get Conversation History
```python
def get_conversation_history(
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0
) -> List[Message]:
    """Get messages for a conversation (chronological order)"""
    return session.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.asc())\
        .limit(limit)\
        .offset(offset)\
        .all()
```

#### 3. Add Message to Conversation
```python
def add_message(
    conversation_id: UUID,
    role: MessageRole,
    content: str
) -> Message:
    """Add a message to conversation and update conversation.updated_at"""
    # Create message
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    session.add(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()

    session.commit()
    session.refresh(message)
    return message
```

#### 4. Get User's Recent Conversations
```python
def get_user_conversations(
    user_id: str,
    limit: int = 10
) -> List[Conversation]:
    """Get user's most recent conversations"""
    return session.query(Conversation)\
        .filter(Conversation.user_id == user_id)\
        .order_by(Conversation.updated_at.desc())\
        .limit(limit)\
        .all()
```

#### 5. Get Conversation with Validation
```python
def get_conversation_for_user(
    conversation_id: UUID,
    user_id: str
) -> Optional[Conversation]:
    """Get conversation ensuring it belongs to user (security check)"""
    return session.query(Conversation)\
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )\
        .first()
```

---

## Data Integrity Rules

### Validation Constraints

1. **Conversation Constraints**:
   - `id` must be valid UUID v4
   - `user_id` must exist in users table
   - `updated_at` >= `created_at`

2. **Message Constraints**:
   - `id` must be valid UUID v4
   - `conversation_id` must exist in conversations table
   - `role` must be "user" or "assistant"
   - `content` length: 1-10,000 characters
   - `created_at` must be within conversation's time range

3. **User Isolation**:
   - Every conversation query MUST filter by `user_id`
   - Messages accessed only through owned conversations
   - MCP tools validate ownership before any operation

### Cascade Behavior

- **User deleted** → All conversations deleted → All messages deleted
- **Conversation deleted** → All messages deleted
- **Task deleted** → No effect on conversations

---

## Performance Considerations

### Index Strategy
- **conversations.user_id**: Fast user conversation lookups
- **conversations.(user_id, updated_at)**: Ordered recent conversations
- **messages.conversation_id**: Fast message retrieval
- **messages.(conversation_id, created_at)**: Chronological message ordering

### Query Optimization
- **Limit history retrieval**: Default 50 messages, paginate if needed
- **Connection pooling**: Use SQLAlchemy pool (10-20 connections)
- **Avoid N+1 queries**: Use `joinedload` for relationships when needed

### Data Retention (Optional Future)
- Archive conversations older than 90 days
- Summarize long conversations (>100 messages)
- Implement soft deletes for audit trails

---

## State Transitions

### Conversation Lifecycle
```
[NULL] → create_conversation() → [ACTIVE]
[ACTIVE] → add_message() → [ACTIVE] (updated_at refreshed)
[ACTIVE] → delete_conversation() → [DELETED]
```

### Message Lifecycle
```
[NULL] → add_message() → [STORED]
[STORED] → (immutable, no updates)
[STORED] → cascade_delete → [DELETED]
```

---

## Testing Considerations

### Unit Tests (Database Layer)
```python
def test_create_conversation():
    conversation = create_conversation(user_id="test-user")
    assert conversation.id is not None
    assert conversation.user_id == "test-user"
    assert conversation.created_at is not None

def test_add_message_updates_conversation_timestamp():
    conversation = create_conversation(user_id="test-user")
    original_updated_at = conversation.updated_at

    time.sleep(0.1)  # Small delay
    add_message(conversation.id, MessageRole.USER, "Hello")

    updated_conversation = session.get(Conversation, conversation.id)
    assert updated_conversation.updated_at > original_updated_at
```

### Integration Tests (User Isolation)
```python
def test_user_cannot_access_other_user_conversation():
    # User 1 creates conversation
    conv1 = create_conversation(user_id="user-1")

    # User 2 tries to access it
    result = get_conversation_for_user(conv1.id, user_id="user-2")

    assert result is None  # User 2 cannot access user 1's conversation
```

---

## Summary

**New Tables**: 2 (conversations, messages)
**New Relationships**: 2 foreign keys
**Indexes Added**: 4 (user_id, conversation_id, composite indexes)
**Migration Script**: `002_add_conversations.py`
**State Management**: Fully database-persisted (stateless backend compliant)
**User Isolation**: Enforced via foreign keys + query filters

---

**Data Model Complete**: Ready for contract generation (MCP tools, Chat API).
