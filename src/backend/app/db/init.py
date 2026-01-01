"""Initialize database tables."""
from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task
from app.models.conversation import Conversation
from app.models.message import Message
from app.db.config import engine


def init_db():
    """Create all tables in the database."""
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database tables created successfully.")
