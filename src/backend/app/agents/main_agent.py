"""
Main Orchestrator Agent

Coordinates all subagents and skills to process user messages.

Constitution Compliance:
- Agent-first design: Business logic in agents (§2.3)
- Coordinates subagents + skills (§5.2, §5.3)
- Uses MCP as only system interface (§2.4)
"""

from typing import Dict, Any, Optional
from uuid import UUID
import logging
from sqlmodel import Session

from app.mcp.server import MCPServer
from app.agents.subagents.task_reasoning import task_reasoning_subagent, TaskDecision
from app.agents.subagents.conversation_memory import conversation_memory_subagent
from app.agents.subagents.tool_orchestration import create_tool_orchestration_subagent
from app.agents.subagents.response_formatting import response_formatting_subagent

logger = logging.getLogger(__name__)


class TodoChatAgent:
    """
    Main orchestrator agent for todo chatbot

    Responsibilities:
    - Coordinate all subagents
    - Process user messages
    - Execute tool calls via MCP
    - Format responses

    Constitution Compliance:
    - Never accesses database directly (§2.4)
    - All operations through MCP (§2.4)
    - Stateless (§2.5)
    """

    def __init__(self, mcp_server: MCPServer, db_session: Session):
        """
        Initialize main agent

        Args:
            mcp_server: MCP server instance
            db_session: Database session for loading conversation history
        """
        self.mcp_server = mcp_server
        self.db_session = db_session

        # Initialize subagents
        self.task_reasoner = task_reasoning_subagent
        self.memory = conversation_memory_subagent
        self.orchestrator = create_tool_orchestration_subagent(mcp_server)
        self.formatter = response_formatting_subagent

        logger.info("TodoChatAgent initialized")

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[UUID] = None
    ) -> str:
        """
        Process a user message and generate response

        Args:
            user_id: User ID (from JWT)
            message: User's natural language input
            conversation_id: Optional conversation ID for context

        Returns:
            AI assistant's response
        """
        logger.info(f"Processing message for user {user_id}: {message[:50]}...")

        try:
            # Load conversation context if available
            context = await self._load_context(conversation_id) if conversation_id else {}

            # Step 1: Reason about user intent
            decision: TaskDecision = await self.task_reasoner.reason(message, context)

            # Step 2: Handle clarification needs
            if decision.needs_clarification:
                logger.info("User input needs clarification")
                return decision.clarification_message or "I'm not sure what you'd like to do. Can you provide more details?"

            # Step 3: If no tool needed (e.g., help), return formatted message
            if not decision.tool_name:
                return decision.clarification_message or self.formatter.format_help()

            # Step 4: Execute MCP tool
            logger.info(f"Executing tool: {decision.tool_name}")
            tool_result = await self.orchestrator.execute_tool(
                tool_name=decision.tool_name,
                user_id=user_id,
                parameters=decision.parameters
            )

            # Step 5: Format response based on tool result
            response = await self._format_tool_response(
                decision.tool_name,
                tool_result,
                decision.parameters
            )

            return response

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            return "I'm sorry, something went wrong. Please try again."

    async def _load_context(self, conversation_id: UUID) -> Dict[str, Any]:
        """
        Load conversation context

        Args:
            conversation_id: Conversation UUID

        Returns:
            Context dictionary
        """
        try:
            history = await self.memory.load_history(
                conversation_id,
                self.db_session,
                max_messages=50
            )

            # Extract task references
            task_refs = self.memory.extract_task_references(history)

            return {
                "history": history,
                "task_references": task_refs
            }

        except Exception as e:
            logger.warning(f"Could not load conversation context: {str(e)}")
            return {}

    async def _format_tool_response(
        self,
        tool_name: str,
        tool_result: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> str:
        """
        Format MCP tool result into user-friendly response

        Args:
            tool_name: Name of executed tool
            tool_result: Tool execution result
            parameters: Tool parameters

        Returns:
            Formatted response string
        """
        # Handle errors
        if not tool_result.get("success", True):
            error = tool_result.get("error", {})
            return self.formatter.format_error(error)

        # Get data from result
        data = tool_result.get("data", {})

        # Format based on tool type
        if tool_name == "add_task":
            return self.formatter.format_task_added(data)

        elif tool_name == "list_tasks":
            tasks = data.get("tasks", [])
            filter_type = parameters.get("filter_type", "all")
            return self.formatter.format_task_list(tasks, filter_type)

        elif tool_name == "view_task":
            task = data
            title = task.get("title")
            desc = task.get("description")
            completed = task.get("completed")
            created = task.get("created_at", "")
            updated = task.get("updated_at", "")

            status_emoji = "✅" if completed else "⏳"
            status_text = "Completed" if completed else "Pending"

            response = f"{status_emoji} **Task #{task.get('id')}: {title}**\n\n"
            response += f"📊 Status: {status_text}\n"
            if desc:
                response += f"📝 Description: {desc}\n"
            response += f"📅 Created: {created}\n"
            response += f"🔄 Last updated: {updated}\n\n"
            response += "What would you like to do with this task?"

            return response

        elif tool_name == "update_task":
            task_id = parameters.get("task_id")
            new_title = parameters.get("title") or parameters.get("new_title")
            new_description = parameters.get("description")
            if new_description:
                return f"✅ Task {task_id} updated to '{new_title}' with description: {new_description}"
            return self.formatter.format_task_updated(task_id, new_title)

        elif tool_name == "complete_task":
            task_id = parameters.get("task_id")
            title = data.get("title")
            return self.formatter.format_task_completed(task_id, title)

        elif tool_name == "delete_task":
            task_id = parameters.get("task_id")
            title = data.get("title")
            return self.formatter.format_task_deleted(task_id, title)

        # Fallback
        return self.formatter.format_success("Done", "")


def create_todo_chat_agent(mcp_server: MCPServer, db_session: Session) -> TodoChatAgent:
    """Factory function to create agent instance"""
    return TodoChatAgent(mcp_server, db_session)
