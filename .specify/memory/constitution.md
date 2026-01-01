# Phase III Constitution
<!-- AI-Powered Todo Chatbot: Reusable Intelligence Architecture -->

## 1. Purpose

This Constitution governs **Phase III** of the *Evolution of Todo* project.
It defines the **non-negotiable principles, constraints, and architectural laws** that guide the transformation from a traditional web application into a **conversational, agent-driven chatbot** using **Spec-Driven Development** and establishing **Reusable Intelligence Architecture**.

This document exists to ensure:

- Architectural consistency
- Security by design
- AI-native development discipline
- Strict separation of concerns
- Reproducibility through specifications
- **Agent-first architecture**
- **Reusable intelligence patterns**
- **Stateless, cloud-native design**

---

## 2. Governing Principles

### 2.1 Spec-Driven Development Is Mandatory

All implementation MUST originate from written specifications.

- No feature may be implemented without an approved spec
- Claude Code MUST be the sole code-generation agent
- Manual code writing is strictly prohibited
- Incorrect behavior MUST be fixed by refining the specification, never the code

---

### 2.2 Constitution → Specs → Code (Strict Hierarchy)

The development hierarchy is immutable:

1. **Constitution** — Governing laws
2. **Specifications** — What to build and how it behaves
3. **Claude Code Output** — Generated implementation

If generated code violates this Constitution or any approved specification, the **specification must be corrected**, not the implementation.

---

### 2.3 Agent-First Design (NEW)

Business logic MUST live in **AI agents**, not controllers.

- FastAPI acts only as: transport layer, auth verification, and persistence gateway
- All task management reasoning lives in agents
- Direct database access by agents is **forbidden**

---

### 2.4 MCP as the Only System Interface (NEW)

Agents may **only** interact with the system through MCP tools.

- Direct database access by agents is forbidden
- SQLModel queries must be wrapped in MCP tools
- All state changes go through MCP

---

### 2.5 Stateless Backend (NEW)

Backend services MUST store **zero in-memory state**.

- Conversation and task state persist in the database
- System must be restart-safe
- No session storage in memory

---

### 2.6 Reusable Intelligence Mandate (NEW)

Intelligence must be modular and reusable in:
- Phase IV (Kubernetes deployment)
- Phase V (Event-Driven + Kafka architecture)

Subagents and skills must be designed for composability.

---

## 3. Scope of Phase III

Phase III converts the Todo web application into an **AI-powered conversational chatbot**.

### Included

- Natural language task management
- OpenAI Agents SDK integration
- MCP server for system operations
- Subagent architecture (task reasoning, conversation memory, tool orchestration, response formatting)
- Agent skills (intent parsing, MCP invocation, error recovery, summarization)
- Chat API endpoint
- Conversation persistence
- OpenAI ChatKit frontend

### Excluded

- Voice interfaces (future phases)
- Multilingual support (future phases)
- Kubernetes deployment (Phase IV)
- Event-driven architecture (Phase V)
- Advanced task features (recurring, reminders, etc.)

---

## 4. Mandatory Feature Set (Conversational Interface)

Phase III MUST implement all five **Basic Level** Todo features through **natural language**:

1. Add Task (via chat: "add buy milk")
2. Delete Task (via chat: "delete task 3")
3. Update Task (via chat: "change task 2 to buy eggs")
4. View Task List (via chat: "show my tasks")
5. Mark Task as Complete (via chat: "complete task 1")

All task operations MUST be:

- **Natural language driven**
- Authenticated (JWT)
- User-scoped
- Persisted in the database
- Executed through MCP tools only

---

## 5. Architecture Laws

### 5.1 Agent-Driven Architecture (Required)

The system MUST follow this architecture:

```
Frontend (OpenAI ChatKit)
    ↓
Chat API (FastAPI /api/{user_id}/chat)
    ↓
OpenAI Agent (with subagents + skills)
    ↓
MCP Tools (add_task, list_tasks, update_task, complete_task, delete_task)
    ↓
SQLModel ORM
    ↓
Database (Neon PostgreSQL)
```

**Critical Rules:**
- Agents may ONLY interact via MCP tools
- No direct database access by agents
- FastAPI is a thin transport/auth layer

---

### 5.2 Required Subagents (Reusable Intelligence)

Phase III MUST implement these subagents:

1. **Task Reasoning Subagent**
   - Understand user intent
   - Decide which MCP tool(s) to invoke
   - Reusable for: event-driven flows, automation, future microservices

2. **Conversation Memory Subagent**
   - Load conversation history
   - Summarize long conversations
   - Build agent context
   - Reusable for: long sessions, multi-agent orchestration, voice & multilingual chat

3. **Tool Orchestration Subagent**
   - Validate parameters
   - Chain MCP tools
   - Handle multi-step actions
   - Reusable for: Kafka workflows, background jobs, AI automation pipelines

4. **Response Formatting Subagent**
   - Generate human-friendly replies
   - Confirm actions
   - Handle errors gracefully
   - Reusable for: voice output, Urdu support, UI-specific responses

---

### 5.3 Required Agent Skills

Skills must be **generic, composable, and reusable**:

1. **Intent Parsing Skill**
   - Detect CRUD intent
   - Extract task titles, IDs, filters

2. **MCP Tool Invocation Skill**
   - Convert decisions → MCP calls
   - Validate required fields

3. **Error Recovery Skill**
   - Handle missing tasks
   - Ask clarifying questions
   - Retry safely

4. **Conversation Summarization Skill**
   - Compress long history
   - Preserve semantic meaning

---

### 5.4 Monorepo Requirement

Phase III continues the **single monorepo** structure with:

- Unified Spec-Kit context
- Separate frontend and backend directories
- Shared specifications
- `/specs/agents/` directory for subagent and skill specs

This structure is mandatory to allow Claude Code full cross-stack visibility.

---

## 6. Technology Mandates

### 6.1 Frontend

- **OpenAI ChatKit** (conversational UI)
- TypeScript
- Real-time chat interface
- JWT token management

---

### 6.2 Backend

- Python **FastAPI**
- Chat API endpoint (`POST /api/{user_id}/chat`)
- Stateless request handling
- JWT verification middleware

---

### 6.3 AI Framework

- **OpenAI Agents SDK (Python)**
  - Authoritative Reference: https://openai.github.io/openai-agents-python/
- Subagents for modularity
- Agent skills for reusability
- Tool calling via MCP

---

### 6.4 MCP Server

- **Official MCP SDK**
- Required tools:
  - `add_task`
  - `list_tasks`
  - `update_task`
  - `complete_task`
  - `delete_task`
- All tools must validate `user_id`
- No cross-user data leakage

---

### 6.5 Database

- **Neon Serverless PostgreSQL**
- **SQLModel ORM**
- Persistent storage for:
  - Tasks
  - Conversations
  - Messages
- Additional tables:
  - `conversations` (id, user_id, created_at, updated_at)
  - `messages` (id, conversation_id, role, content, created_at)

---

## 7. Authentication & Security Constitution

### 7.1 Authentication Is Mandatory

- Chat API endpoint MUST require authentication
- Anonymous or public access is prohibited
- JWT token must be validated before processing messages

---

### 7.2 JWT-Based Authorization

- Better Auth MUST issue JWT tokens
- Frontend MUST attach JWT tokens to every chat request
- Backend MUST validate JWT tokens on every request
- JWT signing secret MUST be shared via environment variables

---

### 7.3 User Isolation Law

- Users may access ONLY their own:
  - Tasks
  - Conversations
  - Messages
- Cross-user data access is strictly forbidden
- User identity MUST be derived from verified JWT claims
- Ownership MUST be enforced at:
  - MCP tool level
  - Database query level

Any violation of user isolation invalidates Phase III.

---

### 7.4 MCP Tool Security

- All MCP tools MUST validate `user_id` parameter
- Tools MUST reject requests without valid `user_id`
- Tools MUST enforce ownership before any CRUD operation
- No MCP tool may access data across users

---

## 8. Chat API Design Rules

### 8.1 Chat Endpoint

- Endpoint: `POST /api/{user_id}/chat`
- Request body:
  ```json
  {
    "message": "string",
    "conversation_id": "string | null"
  }
  ```
- Response:
  ```json
  {
    "response": "string",
    "conversation_id": "string"
  }
  ```

---

### 8.2 Stateless Request Flow

Every chat request MUST:

1. Authenticate user (JWT)
2. Load conversation history from database
3. Append user message to history
4. Run OpenAI Agent with:
   - Conversation context
   - Subagents
   - Skills
   - MCP tools
5. Execute MCP tool(s) as needed
6. Store assistant response in database
7. Return response to client

The server MUST be restart-safe. No in-memory session state.

---

### 8.3 General API Rules

- All responses MUST be JSON
- HTTP status codes MUST be semantically correct
- Errors MUST return clear, explicit messages
- All endpoints MUST live under `/api/`

---

## 9. Data Integrity Rules

### 9.1 Task Integrity

- Every task MUST belong to exactly one user
- Task ownership MUST be enforced on every operation
- Deleting a task MUST NOT affect other users' data
- Task identifiers MUST NOT be guessable across users

---

### 9.2 Conversation Integrity

- Every conversation MUST belong to exactly one user
- Every message MUST belong to exactly one conversation
- Conversation history MUST be loaded in chronological order
- Messages MUST preserve role (user | assistant)

---

### 9.3 Persistence Rules

- All state MUST be stored in database tables:
  - `tasks`
  - `conversations`
  - `messages`
- No in-memory state storage
- System must survive restarts without data loss

---

## 10. Specification Requirements

Phase III MUST include specifications for:

- Constitution (this document)
- Chatbot feature specification (`/specs/features/chatbot.md`)
- MCP tools specification (`/specs/api/mcp-tools.md`)
- Subagent specifications:
  - `/specs/agents/task-reasoning.md`
  - `/specs/agents/conversation-memory.md`
  - `/specs/agents/tool-orchestration.md`
  - `/specs/agents/response-formatting.md`
- Agent skills specifications:
  - `/specs/agents/skills/intent-parsing.md`
  - `/specs/agents/skills/mcp-invocation.md`
  - `/specs/agents/skills/error-recovery.md`
  - `/specs/agents/skills/conversation-summarization.md`
- Chat API specification
- Database schema (updated for conversations/messages)

All specifications MUST:

- Be written in Markdown
- Be human-readable
- Be explicitly referenced when invoking Claude Code
- Define reusability boundaries

---

## 11. Claude Code Usage Law

Claude Code MUST:

- Read relevant specifications before generating code
- Design reusable subagents and skills first
- Implement agent architecture before chat endpoint
- Respect all architectural and security constraints
- Never invent features not defined in specifications
- **NEVER create one giant monolithic agent**
- **ALWAYS separate concerns into subagents and skills**

If ambiguity exists, Claude Code MUST stop and request specification clarification.

---

## 12. Forbidden Patterns 🚨

The following are **STRICTLY PROHIBITED**:

❌ One giant monolithic agent
❌ Hard-coded reasoning in route handlers
❌ Tool calls embedded in FastAPI endpoints
❌ Direct database access by agents
❌ In-memory conversation state
❌ Skipping subagent architecture

---

## 13. Required Deliverables (Phase III)

A valid Phase III submission MUST include:

- Public GitHub repository
- Phase III Constitution file (this document)
- `/specs` directory with:
  - Feature specification
  - MCP tools specification
  - All subagent specifications
  - All skill specifications
- Working OpenAI ChatKit frontend
- Working FastAPI backend with:
  - Chat API endpoint
  - OpenAI Agent integration
  - 4 subagents
  - 4 agent skills
  - MCP server with 5 tools
- Updated database schema (conversations, messages)
- Neon PostgreSQL database integration
- Authentication via Better Auth (JWT)
- Root and subproject `CLAUDE.md` files
- README with setup instructions

---

## 14. Evaluation Criteria

Phase III submissions are evaluated on:

- Adherence to Spec-Driven Development
- **Reusable intelligence architecture**
- Correct subagent and skill separation
- MCP-only system interface
- Stateless backend design
- Correct authentication and user isolation
- Natural language understanding quality
- Specification completeness and clarity
- Proper use of Claude Code without manual coding
- Future reusability for Phases IV and V

---

## 15. Behavioral Guarantees

The AI assistant MUST:

- Understand natural language task commands
- Perform correct task operations via MCP tools
- Confirm actions politely and clearly
- Handle ambiguity gracefully
- Resume conversations reliably
- Ask clarifying questions when intent is unclear
- Never hallucinate task data
- Always verify operations through MCP tools

---

## 16. Non-Negotiable Rule

> **If it is not specified, it must not be implemented.**
> **If it is incorrect, the specification must be fixed — never the code.**
> **Reusable intelligence is mandatory — no shortcuts.**

---

**Version**: 3.0.0 | **Ratified**: 2025-12-29 | **Phase**: III — AI-Powered Todo Chatbot (Reusable Intelligence Architecture)
