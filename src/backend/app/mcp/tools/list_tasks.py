"""
List Tasks MCP Tool

Retrieves all tasks for the user with optional filtering.

Constitution Compliance:
- Validates user_id (§7.4)
- Enforces user ownership (§7.4)
- Database access via SQLModel (not direct by agents) (§2.4)
"""

from typing import Dict, Any, List
from sqlmodel import Session, select
from datetime import datetime

from app.mcp.base_tool import BaseMCPTool, MCPToolError, create_success_response, create_error_response
from app.models.task import Task


class ListTasksTool(BaseMCPTool):
    """MCP Tool for listing tasks"""

    async def execute(self, user_id: str, filter_type: str = "all", **kwargs) -> Dict[str, Any]:
        """
        List all tasks for the user

        Args:
            user_id: Owner of the tasks
            filter_type: Filter by status ("all", "pending", "completed")

        Returns:
            Array of task objects
        """
        # Log invocation
        self.log_tool_invocation("list_tasks", user_id, {"filter_type": filter_type})

        # Validate user_id
        self.validate_user_id(user_id)

        # Validate filter_type
        valid_filters = ["all", "pending", "completed"]
        if filter_type not in valid_filters:
            raise MCPToolError(
                code="VALIDATION_ERROR",
                message=f"Invalid filter_type. Must be one of: {', '.join(valid_filters)}",
                details={"field": "filter_type", "value": filter_type}
            )

        try:
            # Build query
            statement = select(Task).where(Task.user_id == user_id)

            # Apply filter
            if filter_type == "pending":
                statement = statement.where(Task.completed == False)
            elif filter_type == "completed":
                statement = statement.where(Task.completed == True)

            # Order by created_at descending (newest first)
            statement = statement.order_by(Task.created_at.desc())

            # Execute query
            tasks = self.db.exec(statement).all()

            # Serialize tasks
            tasks_data = [
                {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]

            # Return success response
            message = self._generate_message(len(tasks_data), filter_type)
            return create_success_response(
                data={"tasks": tasks_data, "count": len(tasks_data)},
                message=message
            )

        except Exception as e:
            raise MCPToolError(
                code="INTERNAL_ERROR",
                message="Failed to retrieve tasks",
                details={"error": str(e)}
            )

    def _generate_message(self, count: int, filter_type: str) -> str:
        """Generate user-friendly message based on results"""
        if count == 0:
            if filter_type == "pending":
                return "You have no pending tasks."
            elif filter_type == "completed":
                return "You have no completed tasks."
            else:
                return "You have no tasks yet."
        else:
            if filter_type == "pending":
                return f"You have {count} pending task{'s' if count != 1 else ''}."
            elif filter_type == "completed":
                return f"You have {count} completed task{'s' if count != 1 else ''}."
            else:
                return f"You have {count} total task{'s' if count != 1 else ''}."


def register_list_tasks_tool(mcp_server, db_session: Session):
    """Register list_tasks tool with MCP server"""
    from app.mcp.server import MCPTool

    tool = MCPTool(
        name="list_tasks",
        description="List all tasks for the user with optional filtering",
        parameters={
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "filter_type": {
                    "type": "string",
                    "description": "Filter by status: 'all', 'pending', or 'completed'",
                    "enum": ["all", "pending", "completed"],
                    "default": "all"
                }
            },
            "required": ["user_id"]
        },
        handler=lambda **kwargs: ListTasksTool(db_session).execute(**kwargs)
    )

    mcp_server.register_tool(tool)
