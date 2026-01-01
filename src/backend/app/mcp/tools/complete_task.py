"""
Complete Task MCP Tool

Marks a task as completed.

Constitution Compliance:
- Validates user_id (§7.4)
- Enforces user ownership (§7.4)
- Database access via SQLModel (not direct by agents) (§2.4)
"""

from typing import Dict, Any
from sqlmodel import Session, select
from datetime import datetime

from app.mcp.base_tool import BaseMCPTool, MCPToolError, create_success_response
from app.models.task import Task


class CompleteTaskTool(BaseMCPTool):
    """MCP Tool for completing tasks"""

    async def execute(self, user_id: str, task_id: int, **kwargs) -> Dict[str, Any]:
        """
        Mark a task as completed

        Args:
            user_id: Owner of the task
            task_id: ID of task to complete

        Returns:
            Updated task object
        """
        # Log invocation
        self.log_tool_invocation("complete_task", user_id, {"task_id": task_id})

        # Validate user_id
        self.validate_user_id(user_id)

        try:
            # Find task
            statement = select(Task).where(Task.id == task_id)
            task = self.db.exec(statement).first()

            if not task:
                raise MCPToolError(
                    code="NOT_FOUND",
                    message=f"Task {task_id} not found",
                    details={"task_id": task_id}
                )

            # Validate ownership
            self.validate_ownership(task.user_id, user_id)

            # Mark as completed
            task.completed = True
            task.updated_at = datetime.utcnow()

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
                message=f"Task {task_id} '{task.title}' marked as complete"
            )

        except MCPToolError:
            raise
        except Exception as e:
            self.db.rollback()
            raise MCPToolError(
                code="INTERNAL_ERROR",
                message="Failed to complete task",
                details={"error": str(e)}
            )


def register_complete_task_tool(mcp_server, db_session: Session):
    """Register complete_task tool with MCP server"""
    from app.mcp.server import MCPTool

    tool = MCPTool(
        name="complete_task",
        description="Mark a task as completed",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "task_id": {"type": "integer", "description": "Task ID to complete"}
            },
            "required": ["user_id", "task_id"]
        },
        handler=lambda **kwargs: CompleteTaskTool(db_session).execute(**kwargs)
    )

    mcp_server.register_tool(tool)
