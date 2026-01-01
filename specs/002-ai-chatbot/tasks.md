# Tasks: AI-Powered Todo Chatbot

**Feature**: 002-ai-chatbot
**Branch**: 002-ai-chatbot
**Input**: Design documents from `/specs/002-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL in this project. No test tasks included per feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

---

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **Checkbox**: All tasks start with `- [ ]` (markdown checkbox)
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, etc.)
- Include exact file paths in descriptions

---

## User Story Mapping

Phase III user journeys map to implementation stories:

- **US1**: Add Task (Journey 2) - P1 MVP
- **US2**: List Tasks (Journey 3) - P1 MVP
- **US3**: Update Task (Journey 4) - P2
- **US4**: Complete Task (Journey 5) - P2
- **US5**: Delete Task (Journey 6) - P2
- **US6**: Multi-Step Conversation (Journey 7) - P3
- **US7**: Handle Ambiguity (Journey 8) - P3
- **US8**: Resume Conversation (Journey 9) - P3
- **US9**: Error Handling (Journey 10) - P3

**MVP Scope**: US1 (Add Task) + US2 (List Tasks) provide core conversational functionality

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directory structure per plan.md (backend/src/{models,agents,mcp,api}, frontend/src/{components,pages,services})
- [X] T002 Install Python 3.13+ dependencies: FastAPI, SQLModel, openai-agents-sdk, mcp-sdk in backend/requirements.txt
- [X] T003 [P] Install frontend dependencies: OpenAI ChatKit, TypeScript, React in frontend/package.json
- [X] T004 [P] Configure environment variables: OpenAI API key, database URL, JWT secret in backend/.env
- [X] T005 [P] Configure frontend environment: API URL, Better Auth URL in frontend/.env.local

**Checkpoint**: Project structure ready, dependencies installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Models

- [X] T006 Create Conversation model in backend/src/models/conversation.py (UUID, user_id, created_at, updated_at)
- [X] T007 [P] Create Message model in backend/src/models/message.py (UUID, conversation_id, role enum, content, created_at)
- [X] T008 Generate Alembic migration for conversations and messages tables in backend/alembic/versions/002_add_conversations.py
- [X] T009 Run database migration: alembic upgrade head (migration file ready, run manually when DB is available)

### MCP Server Foundation

- [X] T010 [P] Create MCP server initialization in backend/src/mcp/server.py (MCPServer setup, tool registration)
- [X] T011 [P] Create MCP base tool interface in backend/src/mcp/base_tool.py (user_id validation, ownership checks)

### Agent Skills (Reusable Components)

- [X] T012 [P] Implement Intent Parsing Skill in backend/src/agents/skills/intent_parsing.py (parse natural language → intent enum)
- [X] T013 [P] Implement MCP Invocation Skill in backend/src/agents/skills/mcp_invocation.py (invoke MCP tools with validation)
- [X] T014 [P] Implement Error Recovery Skill in backend/src/agents/skills/error_recovery.py (handle errors, ask clarifying questions)
- [X] T015 [P] Implement Conversation Summarization Skill in backend/src/agents/skills/conversation_summarization.py (compress long histories)

### Agent Subagents (Specialized Components)

- [X] T016 [P] Implement Task Reasoning Subagent in backend/src/agents/subagents/task_reasoning.py (understand intent, decide MCP tool)
- [X] T017 [P] Implement Conversation Memory Subagent in backend/src/agents/subagents/conversation_memory.py (load history, build context)
- [X] T018 [P] Implement Tool Orchestration Subagent in backend/src/agents/subagents/tool_orchestration.py (validate params, chain tools)
- [X] T019 [P] Implement Response Formatting Subagent in backend/src/agents/subagents/response_formatting.py (generate friendly responses)

### Main Agent Orchestrator

- [X] T020 Create Main Orchestrator Agent in backend/src/agents/main_agent.py (coordinate subagents + skills, OpenAI integration)

### Chat API Infrastructure

- [X] T021 [P] Create JWT authentication middleware in backend/src/api/auth.py (validate JWT, extract user_id) - Using existing Phase II middleware
- [X] T022 [P] Create conversation service in backend/src/services/conversation_service.py (CRUD operations for conversations/messages)

**Checkpoint**: Foundation ready - all core infrastructure in place, user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task via Chat (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks through natural language like "Add buy groceries"

**Independent Test**: User can send "Add buy milk" and task is created in database with confirmation

**User Journey**: Journey 2 (Adding a Task)

### MCP Tool for User Story 1

- [X] T023 [US1] Implement add_task MCP tool in backend/src/mcp/tools/add_task.py (validate user_id, create task via SQLModel, return task object)

### Chat API for User Story 1

- [X] T024 [US1] Implement POST /api/{user_id}/chat endpoint in backend/src/api/chat.py (authenticate, load history, run agent, store response)
- [X] T025 [US1] Integrate main agent with chat endpoint (pass MCP client, conversation context)

### Frontend for User Story 1

- [X] T026 [P] [US1] Create ChatInterface component in frontend/src/components/ChatInterface.tsx (OpenAI ChatKit integration)
- [X] T027 [P] [US1] Create chat page in frontend/src/pages/chat.tsx (render ChatInterface)
- [X] T028 [P] [US1] Implement chat API client in frontend/src/services/chatApi.ts (POST to /api/{user_id}/chat with JWT)
- [X] T029 [P] [US1] Create useChat hook in frontend/src/hooks/useChat.ts (manage chat state, handle messages)

**Checkpoint**: User can open chat, type "Add buy groceries", and see "✅ Task 'buy groceries' added."

---

## Phase 4: User Story 2 - List Tasks via Chat (Priority: P1) 🎯 MVP

**Goal**: Enable users to view their tasks through natural language like "Show my tasks"

**Independent Test**: User can send "What tasks do I have?" and receive formatted task list

**User Journey**: Journey 3 (Listing Tasks)

### MCP Tool for User Story 2

- [X] T030 [US2] Implement list_tasks MCP tool in backend/src/mcp/tools/list_tasks.py (validate user_id, filter by status, return task array)

### Agent Enhancement for User Story 2

- [X] T031 [US2] Update Task Reasoning Subagent to recognize list intent in backend/src/agents/subagents/task_reasoning.py
- [X] T032 [US2] Update Response Formatting Subagent to format task lists in backend/src/agents/subagents/response_formatting.py

### Frontend Enhancement for User Story 2

- [X] T033 [P] [US2] Add custom task list renderer in frontend/src/components/TaskMessageRenderer.tsx (format task lists nicely)

**Checkpoint**: User can type "Show my tasks" and see all their tasks listed (pending and completed distinguished)

---

## Phase 5: User Story 3 - Update Task via Chat (Priority: P2)

**Goal**: Enable users to update tasks through natural language like "Change task 3 to buy organic groceries"

**Independent Test**: User can send "Update task 1 to buy milk" and task title is updated

**User Journey**: Journey 4 (Updating a Task)

### MCP Tool for User Story 3

- [X] T034 [US3] Implement update_task MCP tool in backend/src/mcp/tools/update_task.py (validate user_id, check ownership, update title/description)

### Agent Enhancement for User Story 3

- [X] T035 [US3] Update Task Reasoning Subagent to recognize update intent and extract task_id + new values in backend/src/agents/subagents/task_reasoning.py

**Checkpoint**: User can type "Change task 2 to buy eggs" and see "✅ Task 2 updated to 'buy eggs'."

---

## Phase 6: User Story 4 - Complete Task via Chat (Priority: P2)

**Goal**: Enable users to mark tasks complete through natural language like "Mark task 2 as done"

**Independent Test**: User can send "Complete task 1" and task status changes to completed

**User Journey**: Journey 5 (Completing a Task)

### MCP Tool for User Story 4

- [X] T036 [US4] Implement complete_task MCP tool in backend/src/mcp/tools/complete_task.py (validate user_id, check ownership, set completed=true)

### Agent Enhancement for User Story 4

- [X] T037 [US4] Update Task Reasoning Subagent to recognize complete intent and extract task_id in backend/src/agents/subagents/task_reasoning.py

**Checkpoint**: User can type "Done with task 1" and see "✅ Task 1 marked as complete."

---

## Phase 7: User Story 5 - Delete Task via Chat (Priority: P2)

**Goal**: Enable users to delete tasks through natural language like "Delete task 4"

**Independent Test**: User can send "Remove task 1" and task is permanently deleted from database

**User Journey**: Journey 6 (Deleting a Task)

### MCP Tool for User Story 5

- [X] T038 [US5] Implement delete_task MCP tool in backend/src/mcp/tools/delete_task.py (validate user_id, check ownership, delete from database)

### Agent Enhancement for User Story 5

- [X] T039 [US5] Update Task Reasoning Subagent to recognize delete intent and extract task_id in backend/src/agents/subagents/task_reasoning.py

**Checkpoint**: User can type "Delete task 3" and see "✅ Task 3 deleted."

---

## Phase 8: User Story 6 - Multi-Step Conversation (Priority: P3)

**Goal**: Enable AI to maintain context across multiple messages (e.g., "Show tasks" → "Complete the first one")

**Independent Test**: User sends "Show my tasks" then "Complete the first one" and first task is marked complete

**User Journey**: Journey 7 (Multi-Step Conversation)

### Implementation for User Story 6

- [X] T040 [US6] Enhance Conversation Memory Subagent to store task list in context in backend/src/agents/subagents/conversation_memory.py
- [X] T041 [US6] Enhance Task Reasoning Subagent to resolve references ("the first one") in backend/src/agents/subagents/task_reasoning.py
- [X] T042 [US6] Update conversation service to properly order messages chronologically in backend/src/services/conversation_service.py

**Checkpoint**: User can have multi-turn dialogue with context preserved (e.g., "Show tasks" → "Complete the second one")

---

## Phase 9: User Story 7 - Handle Ambiguity (Priority: P3)

**Goal**: Enable AI to ask clarifying questions when user input is incomplete

**Independent Test**: User sends "Update the task" and AI responds with "Which task would you like to update?"

**User Journey**: Journey 8 (Handling Ambiguity)

### Implementation for User Story 7

- [X] T043 [US7] Enhance Task Reasoning Subagent to detect insufficient parameters in backend/src/agents/subagents/task_reasoning.py
- [X] T044 [US7] Enhance Error Recovery Skill to generate clarifying questions in backend/src/agents/skills/error_recovery.py
- [X] T045 [US7] Update Response Formatting Subagent to format clarifying questions in backend/src/agents/subagents/response_formatting.py

**Checkpoint**: User can send ambiguous input ("Update task") and AI asks clarifying questions until enough info is gathered

---

## Phase 10: User Story 8 - Resume Conversation (Priority: P3)

**Goal**: Enable users to resume previous conversations with full context

**Independent Test**: User starts conversation, closes browser, returns later, and conversation history is loaded

**User Journey**: Journey 9 (Resuming a Conversation)

### Implementation for User Story 8

- [X] T046 [US8] Implement get_user_conversations query in backend/src/services/conversation_service.py (list user's recent conversations)
- [X] T047 [US8] Update chat endpoint to accept existing conversation_id in backend/src/api/chat.py
- [ ] T048 [US8] Add conversation list UI in frontend/src/components/ConversationList.tsx (show recent conversations)
- [ ] T049 [US8] Update useChat hook to load existing conversations in frontend/src/hooks/useChat.ts

**Checkpoint**: User can close and reopen chat, select previous conversation, and context is fully restored

---

## Phase 11: User Story 9 - Error Handling (Priority: P3)

**Goal**: Enable graceful error handling (e.g., "Delete task 999" → "Task not found. Would you like to see your tasks?")

**Independent Test**: User sends "Delete task 999" and receives helpful error message

**User Journey**: Journey 10 (Error Handling)

### Implementation for User Story 9

- [X] T050 [US9] Update all MCP tools to return structured errors in backend/src/mcp/tools/*.py
- [X] T051 [US9] Enhance Error Recovery Skill to handle MCP tool errors in backend/src/agents/skills/error_recovery.py
- [X] T052 [US9] Update Response Formatting Subagent to format error messages helpfully in backend/src/agents/subagents/response_formatting.py

**Checkpoint**: User can trigger errors (invalid task IDs, missing params) and receive helpful, actionable error messages

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and system-wide improvements

### Performance Optimization

- [X] T053 [P] Add database indexes on conversations.user_id and messages.conversation_id in migration
- [X] T054 [P] Implement conversation history pagination (limit to 50 messages) in backend/src/services/conversation_service.py
- [ ] T055 [P] Add OpenAI API retry logic with exponential backoff in backend/src/agents/main_agent.py

### Security Hardening

- [X] T056 [P] Add input validation (max message length 5000 chars) in backend/src/api/chat.py
- [ ] T057 [P] Add rate limiting on chat endpoint (10 requests/minute per user) in backend/src/api/chat.py
- [X] T058 [P] Add audit logging for MCP tool invocations in backend/src/mcp/base_tool.py

### Documentation

- [X] T059 [P] Create API documentation with Swagger/OpenAPI in backend/src/main.py
- [ ] T060 [P] Create README with setup instructions at repository root
- [ ] T061 [P] Document MCP tool schemas in backend/src/mcp/README.md

### Deployment Preparation

- [ ] T062 [P] Create Docker configuration for backend in backend/Dockerfile
- [ ] T063 [P] Create Docker configuration for frontend in frontend/Dockerfile
- [ ] T064 [P] Create docker-compose.yml for local development at repository root
- [X] T065 [P] Configure CORS for production in backend/src/main.py

**Checkpoint**: System is production-ready with documentation, security, and deployment configs

---

## Dependencies & Execution Strategy

### Critical Path (Must Complete in Order)

```
Phase 1 (Setup) → Phase 2 (Foundation) → MVP (US1 + US2) → Additional Stories (US3-9) → Polish
```

### User Story Dependencies

- **Foundational**: Phase 2 must complete before ANY user story
- **US1 (Add Task)**: Independent, can start immediately after Phase 2
- **US2 (List Tasks)**: Independent, can start immediately after Phase 2
- **US3 (Update Task)**: Independent, requires US1 or US2 for testing
- **US4 (Complete Task)**: Independent, requires US1 or US2 for testing
- **US5 (Delete Task)**: Independent, requires US1 or US2 for testing
- **US6 (Multi-Step)**: Depends on US1 and US2 (needs context to maintain)
- **US7 (Ambiguity)**: Independent, builds on all CRUD stories
- **US8 (Resume)**: Depends on US1 or US2 (needs conversations to resume)
- **US9 (Error Handling)**: Independent, applies to all stories

### Parallel Execution Opportunities

**After Phase 1 (Setup):**
- T002, T003, T004, T005 can run in parallel (different subsystems)

**Phase 2 (Foundation) - High Parallelism:**
- T006-T009: Database tasks (sequential within group)
- T010-T011: MCP tasks (parallel to database)
- T012-T015: Skills (all parallel, different files)
- T016-T019: Subagents (all parallel, different files)
- T020: Main agent (depends on T012-T019)
- T021-T022: API infrastructure (parallel)

**User Story Implementation:**
- **US1 and US2 can be implemented in parallel** (different MCP tools, different intents)
- **US3, US4, US5 can all be implemented in parallel** (each is one MCP tool + agent enhancement)
- **Frontend tasks within each story are parallelizable** (components, pages, services)

**Polish Phase:**
- T053-T065: Nearly all tasks parallelizable (different concerns)

### Recommended MVP Delivery

**Sprint 1** (Foundation + Core Chat):
- Phase 1: Setup
- Phase 2: Foundational
- Phase 3: US1 (Add Task)
- Phase 4: US2 (List Tasks)

**Result**: Working chatbot that can add and list tasks via natural language

**Sprint 2** (Full CRUD):
- Phase 5: US3 (Update Task)
- Phase 6: US4 (Complete Task)
- Phase 7: US5 (Delete Task)

**Result**: Complete CRUD operations via chat

**Sprint 3** (Advanced Features):
- Phase 8: US6 (Multi-Step)
- Phase 9: US7 (Ambiguity)
- Phase 10: US8 (Resume)
- Phase 11: US9 (Error Handling)

**Result**: Production-ready conversational AI

**Sprint 4** (Polish):
- Phase 12: Polish & Cross-Cutting

**Result**: Hardened, documented, deployable system

---

## Task Statistics

**Total Tasks**: 65

**By Phase**:
- Phase 1 (Setup): 5 tasks
- Phase 2 (Foundational): 17 tasks ⚠️ Critical path
- Phase 3 (US1 - Add Task): 7 tasks 🎯 MVP
- Phase 4 (US2 - List Tasks): 4 tasks 🎯 MVP
- Phase 5 (US3 - Update): 2 tasks
- Phase 6 (US4 - Complete): 2 tasks
- Phase 7 (US5 - Delete): 2 tasks
- Phase 8 (US6 - Multi-Step): 3 tasks
- Phase 9 (US7 - Ambiguity): 3 tasks
- Phase 10 (US8 - Resume): 4 tasks
- Phase 11 (US9 - Error Handling): 3 tasks
- Phase 12 (Polish): 13 tasks

**MVP Task Count**: 33 tasks (Phases 1-4)

**Parallelizable Tasks**: 39 tasks (60% of total)

**User Story Breakdown**:
- US1: 7 tasks (Add Task)
- US2: 4 tasks (List Tasks)
- US3: 2 tasks (Update Task)
- US4: 2 tasks (Complete Task)
- US5: 2 tasks (Delete Task)
- US6: 3 tasks (Multi-Step Conversation)
- US7: 3 tasks (Handle Ambiguity)
- US8: 4 tasks (Resume Conversation)
- US9: 3 tasks (Error Handling)

---

## Format Validation

✅ All tasks follow checklist format: `- [ ] [ID] [P?] [Story?] Description with file path`
✅ All task IDs are sequential (T001-T065)
✅ All [P] markers indicate true parallelism (different files, no blocking dependencies)
✅ All [Story] labels map to user stories (US1-US9)
✅ All descriptions include exact file paths
✅ All user stories have independent test criteria

---

## Implementation Strategy

**Incremental Delivery**: Each user story is independently testable and deliverable

**Test Strategy**: Manual testing per user story (no automated test tasks per specification)

**Reusability Focus**: All agent components (subagents, skills) designed for Phases IV & V

**Constitution Compliance**: All tasks respect agent-first design, MCP-only interface, stateless backend, and reusable intelligence mandates

---

**Ready for Implementation**: Generate code via `/sp.implement` or execute tasks manually with Claude Code following Spec-Driven Development
