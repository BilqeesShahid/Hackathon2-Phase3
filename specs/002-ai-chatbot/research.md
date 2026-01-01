# Research Document: AI-Powered Todo Chatbot

**Feature**: 002-ai-chatbot
**Date**: 2025-12-29
**Phase**: Phase 0 — Research & Design Discovery

---

## 1. OpenAI Agents SDK (Python) — Agent Architecture

### Decision
Use **OpenAI Agents SDK (Python)** with the following architecture:
- **Main orchestrator agent** that coordinates subagents
- **4 specialized subagents** (Task Reasoning, Conversation Memory, Tool Orchestration, Response Formatting)
- **4 reusable skills** (Intent Parsing, MCP Invocation, Error Recovery, Conversation Summarization)
- **Tool calling via MCP** as the only system interface

### Rationale
1. **Official SDK**: OpenAI Agents SDK is the authoritative framework for building agent systems
2. **Subagent pattern**: Enables modular, reusable intelligence components
3. **Skill-based design**: Promotes composability and reuse across phases
4. **Tool calling**: Native support for external tool integration (MCP)

### Alternatives Considered
- **LangChain**: More generic but adds unnecessary complexity
- **Custom agent framework**: Would require building infrastructure from scratch
- **Monolithic agent**: Violates Phase III Constitution (§12 — Forbidden Patterns)

### Implementation Notes

#### Agent Structure
```python
# Main Orchestrator Agent
class TodoChatAgent:
    def __init__(self, mcp_client, subagents, skills):
        self.mcp_client = mcp_client
        self.subagents = {
            'task_reasoning': TaskReasoningSubagent(),
            'conversation_memory': ConversationMemorySubagent(),
            'tool_orchestration': ToolOrchestrationSubagent(),
            'response_formatting': ResponseFormattingSubagent()
        }
        self.skills = {
            'intent_parsing': IntentParsingSkill(),
            'mcp_invocation': MCPInvocationSkill(),
            'error_recovery': ErrorRecoverySkill(),
            'conversation_summarization': ConversationSummarizationSkill()
        }
```

#### Subagent Responsibilities
1. **Task Reasoning Subagent**
   - Parse user intent from natural language
   - Determine which MCP tool(s) to invoke
   - Extract parameters (task IDs, titles, filters)
   - Reusable for: event-driven systems, automation pipelines

2. **Conversation Memory Subagent**
   - Load conversation history from database
   - Maintain context across turns
   - Summarize long conversations (using summarization skill)
   - Reusable for: multi-agent orchestration, voice interfaces

3. **Tool Orchestration Subagent**
   - Validate tool parameters
   - Chain multiple MCP tool calls
   - Handle multi-step operations (e.g., list → filter → complete)
   - Reusable for: Kafka workflows, background jobs

4. **Response Formatting Subagent**
   - Generate human-friendly responses
   - Format task lists for readability
   - Handle error messages gracefully
   - Reusable for: voice output, multilingual support

#### Agent Skills (Composable Functions)
1. **Intent Parsing Skill**
   - Input: Natural language text
   - Output: Intent enum (ADD, LIST, UPDATE, COMPLETE, DELETE) + extracted params
   - Reusable across all conversational features

2. **MCP Tool Invocation Skill**
   - Input: Tool name + parameters
   - Output: Tool result or error
   - Validates user_id is always passed
   - Reusable for any MCP-based operation

3. **Error Recovery Skill**
   - Input: Error message + context
   - Output: Clarifying question or retry strategy
   - Handles missing tasks, invalid IDs, ambiguous inputs
   - Reusable for all error scenarios

4. **Conversation Summarization Skill**
   - Input: Long conversation history
   - Output: Condensed summary preserving key context
   - Used by Conversation Memory Subagent
   - Reusable for long-running sessions

### OpenAI API Configuration

#### Rate Limits & Optimization
- **OpenAI API Rate Limits** (as of 2025):
  - GPT-4: 500 requests/minute, 10,000 tokens/minute (typical tier)
  - GPT-3.5-turbo: 3,500 requests/minute, 90,000 tokens/minute
- **Optimization Strategies**:
  - Use conversation summarization for long histories
  - Cache system prompts
  - Implement exponential backoff on rate limit errors
  - Monitor token usage per request

#### Model Selection
- **Primary Model**: GPT-4 (for production chatbot)
- **Fallback Model**: GPT-3.5-turbo (cost optimization)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 500 (sufficient for task responses)

---

## 2. MCP SDK Integration — System Interface

### Decision
Implement **MCP server using Official MCP SDK (Python)** with:
- 5 MCP tools wrapping SQLModel database operations
- FastAPI integration via custom middleware
- JSON schema validation for tool parameters
- User ownership enforcement at tool level

### Rationale
1. **Official SDK**: MCP SDK is the standard for Model Context Protocol
2. **Clear abstraction**: Agents never touch database directly
3. **Security boundary**: User validation happens at tool level
4. **Reusability**: Same MCP tools can be used in Phases IV & V

### Alternatives Considered
- **Direct database access by agents**: Violates Constitution (§2.4)
- **REST API wrapper**: Adds unnecessary HTTP overhead
- **Custom protocol**: Reinventing the wheel

### Implementation Notes

#### MCP Server Setup
```python
from mcp import MCPServer, Tool, ToolParameter

# Initialize MCP server
mcp_server = MCPServer(name="todo-mcp-server")

# Define tools
@mcp_server.tool(
    name="add_task",
    description="Create a new task for the user",
    parameters=[
        ToolParameter(name="user_id", type="string", required=True),
        ToolParameter(name="title", type="string", required=True),
        ToolParameter(name="description", type="string", required=False)
    ]
)
def add_task(user_id: str, title: str, description: str = None):
    # Validate user ownership
    # Create task via SQLModel
    # Return task object
    pass
```

#### MCP Tools Specification

**1. add_task**
- Parameters: `user_id` (string), `title` (string), `description` (string, optional)
- Returns: Created task object
- Validation: user_id required, title non-empty

**2. list_tasks**
- Parameters: `user_id` (string), `filter` (enum: "all" | "pending" | "completed", default "all")
- Returns: Array of task objects
- Validation: user_id required, filter must be valid enum

**3. update_task**
- Parameters: `user_id` (string), `task_id` (int), `title` (string, optional), `description` (string, optional)
- Returns: Updated task object
- Validation: user_id required, task_id must exist and belong to user, at least one update field

**4. complete_task**
- Parameters: `user_id` (string), `task_id` (int)
- Returns: Completed task object
- Validation: user_id required, task_id must exist and belong to user

**5. delete_task**
- Parameters: `user_id` (string), `task_id` (int)
- Returns: Success confirmation
- Validation: user_id required, task_id must exist and belong to user

#### FastAPI Integration
```python
from fastapi import FastAPI, Depends
from mcp import MCPServer

app = FastAPI()
mcp_server = MCPServer(name="todo-mcp")

# Middleware to inject MCP server into agent context
@app.middleware("http")
async def inject_mcp_client(request, call_next):
    request.state.mcp_client = mcp_server.client()
    response = await call_next(request)
    return response
```

#### Error Handling
- **Tool not found**: Return structured error with available tools list
- **Parameter validation failed**: Return error with required parameters
- **Ownership validation failed**: Return "Task not found" (security best practice)
- **Database error**: Return generic error, log details server-side

---

## 3. OpenAI ChatKit — Conversational UI

### Decision
Use **OpenAI ChatKit (React/TypeScript)** for frontend with:
- Pre-built chat interface components
- JWT token management via custom auth provider
- WebSocket or polling for real-time updates (ChatKit default)
- Custom message rendering for task lists

### Rationale
1. **Official UI library**: ChatKit is designed for OpenAI-powered chat experiences
2. **Rapid development**: Pre-built components accelerate Phase III
3. **Authentication support**: Built-in patterns for token management
4. **Customizable**: Can extend for task-specific formatting

### Alternatives Considered
- **Custom React chat UI**: More work, no immediate benefit
- **Streamlit**: Python-based but less suitable for production web app
- **Next.js Chat Component Library**: Generic, lacks OpenAI integration

### Implementation Notes

#### ChatKit Setup
```typescript
import { ChatProvider, ChatWindow } from '@openai/chatkit';

function ChatPage() {
  const { token } = useAuth(); // JWT from Better Auth

  return (
    <ChatProvider
      apiEndpoint="/api/{user_id}/chat"
      authToken={token}
      userId={userId}
    >
      <ChatWindow
        customMessageRenderer={TaskMessageRenderer}
        placeholder="Ask me to manage your tasks..."
      />
    </ChatProvider>
  );
}
```

#### JWT Token Management
```typescript
// Custom auth provider
const authProvider = {
  getToken: async () => {
    // Get JWT from Better Auth session
    const session = await getSession();
    return session.jwt;
  },
  refreshToken: async () => {
    // Refresh JWT if expired
    return await refreshSession();
  }
};
```

#### Custom Message Rendering
```typescript
// Render task lists nicely
function TaskMessageRenderer({ message }) {
  if (message.type === 'task_list') {
    return (
      <TaskList tasks={message.data.tasks} />
    );
  }
  return <DefaultMessageRenderer message={message} />;
}
```

#### Real-Time Updates
- **ChatKit default**: Polling every 1-2 seconds
- **Optimization**: WebSocket upgrade for production (optional in Phase III)
- **Stateless constraint**: All state from database, no client-side caching beyond session

---

## 4. Testing Strategy — AI Agent Testing

### Decision
Implement **multi-layered testing strategy**:
- **Unit tests**: Individual subagents and skills (mocked dependencies)
- **Integration tests**: Agent + MCP tools (test database)
- **Contract tests**: MCP tool schemas and validation
- **End-to-end tests**: Full chat flow (mocked OpenAI API)

### Rationale
1. **Testability**: Each component (subagent, skill, tool) is independently testable
2. **Mock external APIs**: Avoid OpenAI API costs in tests
3. **Contract validation**: Ensure MCP tools match specifications
4. **Confidence**: E2E tests validate full user journeys

### Alternatives Considered
- **No agent testing**: Risky, violates quality standards
- **Only E2E tests**: Slow, hard to debug, expensive
- **Manual testing only**: Not repeatable, not CI-friendly

### Implementation Notes

#### Unit Testing (pytest)
```python
# Test subagent in isolation
def test_task_reasoning_subagent_add_intent():
    subagent = TaskReasoningSubagent()
    intent = subagent.parse_intent("Add buy milk")
    assert intent.action == IntentAction.ADD
    assert intent.params['title'] == "buy milk"

# Test skill in isolation
def test_intent_parsing_skill():
    skill = IntentParsingSkill()
    result = skill.parse("Show my tasks")
    assert result.intent == "LIST"
    assert result.filter == "all"
```

#### Mocking OpenAI API
```python
# Mock OpenAI responses
@pytest.fixture
def mock_openai(mocker):
    mock_response = {
        'choices': [{
            'message': {
                'content': 'Intent: ADD, Title: buy milk'
            }
        }]
    }
    mocker.patch('openai.ChatCompletion.create', return_value=mock_response)
```

#### MCP Tool Contract Tests
```python
# Validate MCP tool schemas
def test_add_task_tool_schema():
    tool = mcp_server.get_tool("add_task")
    assert tool.name == "add_task"
    assert "user_id" in tool.parameters
    assert tool.parameters["user_id"].required == True
    assert tool.parameters["title"].required == True
```

#### Integration Tests
```python
# Test agent + MCP tools with test database
@pytest.mark.integration
def test_chat_add_task_flow(test_db, mock_openai):
    agent = TodoChatAgent(mcp_client=test_mcp_client)
    response = agent.process_message(
        user_id="test-user",
        message="Add buy groceries"
    )

    # Verify task was created in test DB
    tasks = test_db.query(Task).filter_by(user_id="test-user").all()
    assert len(tasks) == 1
    assert tasks[0].title == "buy groceries"
    assert "added" in response.lower()
```

#### End-to-End Tests
```python
# Test full chat API flow
@pytest.mark.e2e
def test_chat_api_complete_workflow(test_client, mock_openai):
    # Login and get JWT
    token = login_test_user()

    # Send chat message
    response = test_client.post(
        "/api/test-user/chat",
        json={"message": "Show my tasks"},
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert "tasks" in response.json()
```

#### Test Coverage Goals
- **Unit tests**: 90%+ coverage for subagents and skills
- **Integration tests**: All MCP tools + agent interactions
- **Contract tests**: 100% coverage of MCP tool schemas
- **E2E tests**: All 10 user journeys from spec

---

## 5. Database Schema — Conversations & Messages

### Decision
Add **two new tables** to existing schema:
- `conversations`: Stores conversation metadata
- `messages`: Stores individual messages (user + assistant)

### Rationale
1. **Stateless requirement**: All conversation state must persist in database
2. **User isolation**: Conversations belong to users (foreign key)
3. **Chronological history**: Messages ordered by created_at
4. **Scalability**: Indexed queries for efficient history retrieval

### Implementation Notes

#### Conversation Model (SQLModel)
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
```

#### Message Model (SQLModel)
```python
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    role: MessageRole = Field(sa_column=Column(Enum(MessageRole)))
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

#### Database Migrations
- Use Alembic for migrations
- Migration file: `add_conversations_and_messages.py`
- Indexes: `user_id`, `conversation_id`, `created_at`

#### Query Patterns
```python
# Load conversation history (most recent first)
def get_conversation_history(conversation_id: UUID, limit: int = 50):
    return session.query(Message)\
        .filter(Message.conversation_id == conversation_id)\
        .order_by(Message.created_at.desc())\
        .limit(limit)\
        .all()

# Get user's conversations
def get_user_conversations(user_id: str):
    return session.query(Conversation)\
        .filter(Conversation.user_id == user_id)\
        .order_by(Conversation.updated_at.desc())\
        .all()
```

---

## 6. Performance Considerations

### OpenAI API Latency
- **Average response time**: 1-3 seconds for GPT-4
- **Optimization**: Use streaming responses (display tokens as they arrive)
- **Caching**: Cache system prompts to reduce token usage
- **Fallback**: Switch to GPT-3.5-turbo if latency > 5 seconds

### Database Query Optimization
- **Index strategy**: Index on `user_id`, `conversation_id`, `created_at`
- **Pagination**: Limit conversation history to recent 50 messages
- **Connection pooling**: Use SQLAlchemy connection pool (10-20 connections)

### Conversation History Management
- **Summarization threshold**: Summarize conversations > 100 messages
- **Compression**: Store summarized history separately
- **Pruning**: Archive conversations older than 90 days (optional)

---

## 7. Security Considerations

### JWT Validation
- Validate JWT signature on every request
- Extract `user_id` from JWT claims
- Reject expired tokens

### MCP Tool Security
- Always require `user_id` parameter
- Validate task ownership before any operation
- Never expose other users' data in error messages
- Log security-relevant events (failed ownership checks)

### Input Sanitization
- Sanitize user messages before storing
- Prevent SQL injection (SQLModel handles this)
- Validate message length (max 5000 characters)

---

## 8. Deployment Considerations (Phase III Scope)

### Environment Variables
```bash
# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Database
DATABASE_URL=postgresql://...

# Authentication
JWT_SECRET=...
BETTER_AUTH_URL=...

# MCP Server
MCP_SERVER_PORT=8001
```

### Docker Considerations (Future)
- Separate containers for FastAPI backend and MCP server
- Shared database connection
- Health checks for agent availability

---

## Summary of Research Decisions

| Component | Decision | Rationale |
|-----------|----------|-----------|
| Agent Framework | OpenAI Agents SDK | Official, supports subagents/skills |
| System Interface | MCP SDK | Official protocol, clear abstraction |
| Frontend | OpenAI ChatKit | Rapid development, OpenAI integration |
| Testing | Multi-layer (unit, integration, E2E) | Comprehensive coverage, mockable |
| Database | Two new tables (conversations, messages) | Stateless requirement |
| Model | GPT-4 (primary), GPT-3.5-turbo (fallback) | Quality vs. cost balance |
| Rate Limiting | Exponential backoff + caching | Handle OpenAI limits gracefully |

---

**Research Complete**: All unknowns resolved. Ready for Phase 1 (Design & Contracts).
