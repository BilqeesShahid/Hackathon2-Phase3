"""
Update Task MCP Tool

Updates an existing task's title and/or description.

Constitution Compliance:
- Validates user_id (§7.4)
- Enforces user ownership (§7.4)
- Database access via SQLModel (not direct by agents) (§2.4)
"""

from typing import Dict, Any, Optional
from sqlmodel import Session, select

from app.mcp.base_tool import BaseMCPTool, MCPToolError, create_success_response
from app.models.task import Task


class UpdateTaskTool(BaseMCPTool):
    """MCP Tool for updating tasks"""

    async def execute(
        self,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update an existing task

        Args:
            user_id: Owner of the task
            task_id: ID of task to update
            title: New task title (optional)
            description: New task description (optional)

        Returns:
            Updated task object
        """
        # Log invocation
        self.log_tool_invocation("update_task", user_id, {"task_id": task_id})

        # Validate user_id
        self.validate_user_id(user_id)

        # Validate at least one field is being updated
        if not title and description is None:
            raise MCPToolError(
                code="VALIDATION_ERROR",
                message="At least one field (title or description) must be provided",
                details={"task_id": task_id}
            )

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

            # Update fields
            if title:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip() if description else None

            # Update timestamp
            from datetime import datetime
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
                message=f"Task {task_id} updated"
            )

        except MCPToolError:
            raise
        except Exception as e:
            self.db.rollback()
            raise MCPToolError(
                code="INTERNAL_ERROR",
                message="Failed to update task",
                details={"error": str(e)}
            )


def register_update_task_tool(mcp_server, db_session: Session):
    """Register update_task tool with MCP server"""
    from app.mcp.server import MCPTool

    tool = MCPTool(
        name="update_task",
        description="Update an existing task's title or description",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "task_id": {"type": "integer", "description": "Task ID to update"},
                "title": {"type": "string", "description": "New task title (optional)"},
                "description": {"type": "string", "description": "New task description (optional)"}
            },
            "required": ["user_id", "task_id"]
        },
        handler=lambda **kwargs: UpdateTaskTool(db_session).execute(**kwargs)
    )

    mcp_server.register_tool(tool)
