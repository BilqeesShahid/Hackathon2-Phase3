"""
Response Formatting Subagent

Generates human-friendly responses, confirms actions, handles errors gracefully.

Reusability: Voice output, Urdu support, UI-specific responses

Constitution Compliance:
- Behavioral guarantees: Polite confirmations (§15)
- Reusable intelligence (§2.6)
"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class ResponseFormattingSubagent:
    """
    Subagent for formatting AI responses

    Responsibilities:
    - Generate human-friendly responses
    - Confirm actions clearly
    - Format task lists readably
    - Handle errors gracefully
    """

    def format_success(self, action: str, details: str = "") -> str:
        """Format success response"""
        base = f"✅ {details}" if details else f"✅ Done!"
        return base

    def format_task_added(self, task: Dict[str, Any]) -> str:
        """Format task addition confirmation"""
        title = task.get("title", "Task")
        description = task.get("description")
        task_id = task.get("id")

        if description:
            return f"✅ Great! I've added task #{task_id}: '{title}'\n📝 Description: {description}\n\nWhat else can I help you with?"
        else:
            return f"✅ Perfect! I've added task #{task_id}: '{title}'\n\n💡 Tip: Add descriptions using patterns like:\n  • 'Add task - description'\n  • 'Add task, description'\n  • 'Add task (description)'"

    def format_task_list(self, tasks: List[Dict[str, Any]], filter_type: str = "all") -> str:
        """
        Format task list for display

        Args:
            tasks: List of task objects
            filter_type: Filter type (all, pending, completed)

        Returns:
            Formatted task list string
        """
        if not tasks:
            if filter_type == "pending":
                return "🎉 Great news! You have no pending tasks. You're all caught up!\n\nWant to add a new task?"
            elif filter_type == "completed":
                return "You haven't completed any tasks yet. Keep working on your pending tasks!"
            else:
                return "You don't have any tasks yet. Let's get started!\n\nTry saying: 'Add buy groceries'"

        # Group by status if showing all
        if filter_type == "all":
            pending = [t for t in tasks if not t.get("completed", False)]
            completed = [t for t in tasks if t.get("completed", False)]

            lines = [f"📋 Here are your tasks ({len(tasks)} total):"]

            if pending:
                lines.append(f"\n**⏳ Pending Tasks ({len(pending)}):**")
                for task in pending:
                    desc = task.get('description')
                    if desc:
                        lines.append(f"  {task.get('id')}. {task.get('title')}\n     📝 {desc}")
                    else:
                        lines.append(f"  {task.get('id')}. {task.get('title')}")

            if completed:
                lines.append(f"\n**✅ Completed Tasks ({len(completed)}):**")
                for task in completed:
                    lines.append(f"  ~~{task.get('id')}. {task.get('title')}~~")

        else:
            status_label = filter_type.capitalize()
            count = len(tasks)
            lines = [f"📋 Here are your {filter_type} tasks ({count} total):"]
            for task in tasks:
                if task.get("completed"):
                    lines.append(f"  ~~{task.get('id')}. {task.get('title')}~~")
                else:
                    desc = task.get('description')
                    if desc:
                        lines.append(f"  {task.get('id')}. {task.get('title')}\n     📝 {desc}")
                    else:
                        lines.append(f"  {task.get('id')}. {task.get('title')}")

        lines.append("\n💬 What would you like to do next?")
        return "\n".join(lines)

    def format_task_updated(self, task_id: int, new_title: Optional[str] = None) -> str:
        """Format task update confirmation"""
        if new_title:
            return f"✅ Awesome! I've updated task #{task_id} to: '{new_title}'\n\nAnything else you need?"
        return f"✅ Task #{task_id} has been updated successfully!"

    def format_task_completed(self, task_id: int, title: Optional[str] = None) -> str:
        """Format task completion confirmation"""
        if title:
            return f"🎉 Congratulations! Task #{task_id} '{title}' is now complete!\n\nKeep up the great work! What's next?"
        return f"🎉 Task #{task_id} marked as complete! Nice job!"

    def format_task_deleted(self, task_id: int, title: Optional[str] = None) -> str:
        """Format task deletion confirmation"""
        if title:
            return f"🗑️ Got it! I've deleted task #{task_id}: '{title}'\n\nIs there anything else I can help with?"
        return f"🗑️ Task #{task_id} has been deleted."

    def format_error(self, error: Dict[str, Any]) -> str:
        """
        Format error message (user-friendly)

        Args:
            error: Error dict with code and message

        Returns:
            User-friendly error message
        """
        code = error.get("code", "UNKNOWN")
        message = error.get("message", "Something went wrong")

        # Map error codes to friendly messages
        friendly_messages = {
            "NOT_FOUND": "❌ Hmm, I couldn't find that task. Would you like me to show you all your tasks?\n\nTry: 'Show my tasks'",
            "UNAUTHORIZED": "🔒 I need to verify your identity first. Please make sure you're logged in.",
            "VALIDATION_ERROR": f"⚠️ {message}\n\nNeed help? Type 'help' to see what I can do!",
            "INTERNAL_ERROR": "😔 Oops! Something unexpected happened. Please try again.\n\nIf this keeps happening, try: 'Show my tasks' to verify everything is working.",
            "TOOL_NOT_FOUND": f"⚠️ {message}",
        }

        return friendly_messages.get(code, f"❌ {message}")

    def format_clarification(self, question: str, context: Optional[str] = None) -> str:
        """Format clarification question"""
        if context:
            return f"{context}\n\n{question}"
        return question

    def format_help(self) -> str:
        """Format help message"""
        return """🤖 **I'm your AI Task Manager!** Here's what I can do:

📝 **Create tasks**:
   • "Add buy groceries"
   • "Buy milk - get 2 litres" (with description)
   • "Create task call dentist, schedule cleaning"

📋 **View tasks**:
   • "Show my tasks" (all tasks)
   • "Show pending tasks" (only incomplete)
   • "Show completed tasks" (only finished)

✏️ **Update tasks**:
   • "Update task 3 to buy organic milk"
   • "Change task 5 Party planning - send invites by Feb 1"

✅ **Complete tasks**:
   • "Complete task 2"
   • "Mark task 7 as done"
   • "Done with task 4"

🗑️ **Delete tasks**:
   • "Delete task 6"
   • "Remove task 3"

Just talk to me naturally - I understand you! 😊"""

    def format_greeting(self) -> str:
        """Format greeting message"""
        return """👋 Hello! I'm your AI Task Manager!

I can help you manage your tasks using natural language. Just tell me what you need to do!

**Quick examples:**
• "Add buy milk"
• "Show my tasks"
• "Complete task 1"

What would you like to do today?"""


# Singleton instance
response_formatting_subagent = ResponseFormattingSubagent()
