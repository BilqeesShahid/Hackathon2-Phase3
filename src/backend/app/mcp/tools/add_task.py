"""
Add Task MCP Tool

Creates a new task for the user.

Constitution Compliance:
- Validates user_id (§7.4)
- Enforces user ownership (§7.4)
- Database access via SQLModel (not direct by agents) (§2.4)
"""

from typing import Dict, Any
from sqlmodel import Session
from datetime import datetime

from app.mcp.base_tool import BaseMCPTool, MCPToolError, create_success_response, create_error_response
from app.models.task import Task


class AddTaskTool(BaseMCPTool):
    """MCP Tool for adding tasks"""

    async def execute(self, user_id: str, title: str, description: str = None, **kwargs) -> Dict[str, Any]:
        """
        Add a new task

        Args:
            user_id: Owner of the task
            title: Task title
            description: Optional task description

        Returns:
            Created task object
        """
        # Log invocation
        self.log_tool_invocation("add_task", user_id, {"title": title})

        # Validate user_id
        self.validate_user_id(user_id)

        # Validate title
        if not title or not title.strip():
            raise MCPToolError(
                code="VALIDATION_ERROR",
                message="Task title cannot be empty",
                details={"field": "title"}
            )

        try:
            # Create task
            task = Task(
                user_id=user_id,
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)

            # Return success response
            return create_success_response(
                data={
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                },
                message=f"Task '{title}' added"
            )

        except Exception as e:
            self.db.rollback()
            raise MCPToolError(
                code="INTERNAL_ERROR",
                message="Failed to create task",
                details={"error": str(e)}
            )


def register_add_task_tool(mcp_server, db_session: Session):
    """Register add_task tool with MCP server"""
    from app.mcp.server import MCPTool

    tool = MCPTool(
        name="add_task",
        description="Create a new task for the user",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "title": {"type": "string", "description": "Task title"},
                "description": {"type": "string", "description": "Task description (optional)"}
            },
            "required": ["user_id", "title"]
        },
        handler=lambda **kwargs: AddTaskTool(db_session).execute(**kwargs)
    )

    mcp_server.register_tool(tool)
