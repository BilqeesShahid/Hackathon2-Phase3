# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: 002-ai-chatbot
**Phase**: Phase III — AI-Powered Conversational Interface
**Date**: 2025-12-29

---

## Overview

This guide provides setup instructions and development workflow for implementing the AI-powered todo chatbot feature. Follow these steps to set up your development environment and begin implementation.

---

## Prerequisites

### Required Software
- **Python 3.13+** (backend)
- **Node.js 20+** & **npm/yarn** (frontend)
- **PostgreSQL** (via Neon or local)
- **Git** (version control)

### Required Accounts
- **OpenAI API Key** (for OpenAI Agents SDK)
- **Neon Database** (PostgreSQL hosting)
- **Better Auth** (authentication provider)

### Phase II Completion
- ✅ Phase II backend (FastAPI) must be running
- ✅ Phase II database must exist with users and tasks tables
- ✅ Better Auth integration must be functional

---

## Environment Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd hack2-Phase3
git checkout 002-ai-chatbot
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Install New Dependencies for Phase III
```bash
pip install openai-agents-sdk mcp-sdk
pip freeze > requirements.txt
```

#### Configure Environment Variables
Create `.env` file in `backend/` directory:

```bash
# Database
DATABASE_URL=postgresql://user:password@neon-host/dbname

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=500

# Authentication (Better Auth)
JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256
BETTER_AUTH_URL=https://your-auth-url

# MCP Server
MCP_SERVER_PORT=8001
MCP_SERVER_NAME=todo-mcp-server

# Application
ENV=development
LOG_LEVEL=INFO
```

#### Run Database Migrations
```bash
# Create new migration for conversations and messages
alembic revision --autogenerate -m "Add conversations and messages tables"

# Apply migration
alembic upgrade head
```

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd frontend
npm install

# Install OpenAI ChatKit
npm install @openai/chatkit
```

#### Configure Environment Variables
Create `.env.local` file in `frontend/` directory:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-auth-url
```

---

## Project Structure Verification

After setup, your project should have this structure:

```
backend/
├── src/
│   ├── models/
│   │   ├── conversation.py    # NEW
│   │   ├── message.py         # NEW
│   │   └── task.py
│   ├── agents/                # NEW
│   │   ├── main_agent.py
│   │   ├── subagents/
│   │   └── skills/
│   ├── mcp/                   # NEW
│   │   ├── server.py
│   │   └── tools/
│   ├── api/
│   │   ├── chat.py            # NEW
│   │   └── auth.py
│   └── lib/
│       └── database.py
├── tests/
├── .env
└── requirements.txt

frontend/
├── src/
│   ├── components/
│   │   └── ChatInterface.tsx  # NEW
│   ├── pages/
│   │   └── chat.tsx           # NEW
│   ├── services/
│   │   └── chatApi.ts         # NEW
│   └── hooks/
│       └── useChat.ts         # NEW
├── .env.local
└── package.json

specs/
├── 002-ai-chatbot/
│   ├── spec.md
│   ├── plan.md
│   ├── research.md
│   ├── data-model.md
│   ├── quickstart.md          # This file
│   └── contracts/
│       ├── mcp-tools.json
│       └── chat-api.yaml
└── agents/                    # NEW
    ├── task-reasoning.md
    ├── conversation-memory.md
    ├── tool-orchestration.md
    ├── response-formatting.md
    └── skills/
```

---

## Development Workflow

### Phase 1: Database Models (Start Here)
```bash
# 1. Create SQLModel classes
cd backend/src/models
# Create conversation.py (see data-model.md)
# Create message.py (see data-model.md)

# 2. Run migration
alembic revision --autogenerate -m "Add conversations and messages"
alembic upgrade head

# 3. Test models
pytest tests/models/test_conversation.py
pytest tests/models/test_message.py
```

### Phase 2: MCP Tools
```bash
# 1. Create MCP server
cd backend/src/mcp
# Implement server.py

# 2. Create MCP tools (5 tools)
cd tools
# Implement add_task.py
# Implement list_tasks.py
# Implement update_task.py
# Implement complete_task.py
# Implement delete_task.py

# 3. Test MCP tools
pytest tests/mcp/test_tools.py
```

### Phase 3: Agent Architecture
```bash
# 1. Create subagents (4 subagents)
cd backend/src/agents/subagents
# Implement task_reasoning.py
# Implement conversation_memory.py
# Implement tool_orchestration.py
# Implement response_formatting.py

# 2. Create skills (4 skills)
cd backend/src/agents/skills
# Implement intent_parsing.py
# Implement mcp_invocation.py
# Implement error_recovery.py
# Implement conversation_summarization.py

# 3. Create main orchestrator agent
cd backend/src/agents
# Implement main_agent.py

# 4. Test agents
pytest tests/agents/test_subagents.py
pytest tests/agents/test_skills.py
pytest tests/agents/test_main_agent.py
```

### Phase 4: Chat API
```bash
# 1. Create chat endpoint
cd backend/src/api
# Implement chat.py (see chat-api.yaml)

# 2. Test chat API
pytest tests/api/test_chat.py
```

### Phase 5: Frontend Integration
```bash
# 1. Create chat interface component
cd frontend/src/components
# Implement ChatInterface.tsx (OpenAI ChatKit)

# 2. Create chat page
cd frontend/src/pages
# Implement chat.tsx

# 3. Create API client
cd frontend/src/services
# Implement chatApi.ts

# 4. Create chat hook
cd frontend/src/hooks
# Implement useChat.ts

# 5. Test frontend
npm run test
```

### Phase 6: Integration Testing
```bash
# Run end-to-end tests
pytest tests/integration/test_chat_flow.py

# Test all user journeys from spec.md
pytest tests/integration/test_user_journeys.py
```

---

## Running the Application

### Start Backend (Development)
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

### Start MCP Server (Separate Process)
```bash
cd backend
python src/mcp/server.py
```

### Start Frontend (Development)
```bash
cd frontend
npm run dev
```

### Access Application
- Frontend: http://localhost:3000/chat
- Backend API: http://localhost:8000/docs (Swagger UI)
- MCP Server: http://localhost:8001

---

## Testing Strategy

### Unit Tests
```bash
# Test individual components
pytest tests/agents/test_task_reasoning.py
pytest tests/mcp/test_add_task.py
pytest tests/models/test_conversation.py
```

### Integration Tests
```bash
# Test agent + MCP integration
pytest tests/integration/test_agent_mcp.py

# Test full chat flow
pytest tests/integration/test_chat_flow.py
```

### End-to-End Tests
```bash
# Test all user journeys
pytest tests/e2e/test_user_journeys.py -v
```

### Test Coverage
```bash
# Generate coverage report
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

---

## Debugging

### Enable Debug Logging
```python
# In .env
LOG_LEVEL=DEBUG
```

### OpenAI API Debugging
```python
# Log OpenAI API calls
import logging
logging.getLogger("openai").setLevel(logging.DEBUG)
```

### MCP Tool Debugging
```bash
# Test MCP tools directly
python -m mcp.tools.add_task --user_id=test-user --title="Test task"
```

### Database Debugging
```bash
# Inspect database
psql $DATABASE_URL
\dt  # List tables
SELECT * FROM conversations LIMIT 10;
SELECT * FROM messages LIMIT 10;
```

---

## Common Issues & Solutions

### Issue: OpenAI API Rate Limit
**Solution**: Implement exponential backoff
```python
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def call_openai_api():
    return openai.ChatCompletion.create(...)
```

### Issue: Database Connection Pool Exhausted
**Solution**: Increase pool size
```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10
)
```

### Issue: Long Conversation History Slows Down Requests
**Solution**: Implement summarization
```python
# In conversation_memory.py
if len(messages) > 50:
    summarized_history = summarize_conversation(messages[:40])
    recent_messages = messages[-10:]
    context = summarized_history + recent_messages
```

### Issue: JWT Token Expired Mid-Conversation
**Solution**: Frontend auto-refresh
```typescript
// In chatApi.ts
const refreshTokenIfNeeded = async () => {
  const token = await getToken();
  if (isTokenExpired(token)) {
    return await refreshToken();
  }
  return token;
};
```

---

## Code Generation Guidelines

### Using Claude Code for Implementation

**CRITICAL**: All code must be generated from specifications:
1. Read relevant spec file(s)
2. Understand requirements
3. Generate code matching spec exactly
4. No manual coding allowed

**Example: Generating Task Reasoning Subagent**
```
User: "Generate task reasoning subagent according to specs/agents/task-reasoning.md"
Claude Code: [Reads spec, generates backend/src/agents/subagents/task_reasoning.py]
```

### Spec-Driven Development Flow
```
Constitution → Spec → Plan → Research → Design → Tasks → Implementation
     ↓           ↓      ↓        ↓         ↓        ↓           ↓
  Laws      What    How     Unknowns   Details   Steps      Code
```

---

## Deployment Checklist (Phase III Scope)

Before deploying to production:

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All E2E tests passing (10 user journeys)
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] OpenAI API key valid and has sufficient quota
- [ ] JWT secret is strong and secure
- [ ] CORS configured correctly
- [ ] Rate limiting enabled on chat endpoint
- [ ] Error logging configured
- [ ] Health check endpoints responding
- [ ] Database connection pooling optimized
- [ ] Frontend built for production (`npm run build`)

---

## Performance Monitoring

### Key Metrics to Track
- **Chat response time**: Target < 3 seconds p95
- **OpenAI API latency**: Monitor for spikes
- **Database query time**: Optimize slow queries
- **Conversation history retrieval**: Should be < 100ms
- **MCP tool execution**: Each tool < 50ms

### Monitoring Tools
- **Backend**: FastAPI built-in metrics + Prometheus
- **Database**: Neon dashboard + pgAdmin
- **OpenAI**: OpenAI dashboard (usage, rate limits)
- **Frontend**: Vercel Analytics (if deployed on Vercel)

---

## Next Steps After Quickstart

1. **Generate Tasks**: Run `/sp.tasks` to break down implementation into testable tasks
2. **Implement Subagents**: Start with Task Reasoning subagent
3. **Implement Skills**: Start with Intent Parsing skill
4. **Build MCP Tools**: Start with `add_task`
5. **Test Incrementally**: Unit test each component as you build
6. **Integrate Components**: Connect subagents → skills → MCP tools
7. **Build Chat Endpoint**: Integrate OpenAI Agent with FastAPI
8. **Build Frontend**: Integrate OpenAI ChatKit
9. **E2E Testing**: Validate all 10 user journeys
10. **Deploy**: Follow deployment checklist

---

## Additional Resources

### Documentation
- [Phase III Constitution](../../.specify/memory/constitution.md)
- [Feature Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Research Document](./research.md)
- [Data Model](./data-model.md)
- [MCP Tools Schema](./contracts/mcp-tools.json)
- [Chat API Spec](./contracts/chat-api.yaml)

### External Resources
- [OpenAI Agents SDK Docs](https://openai.github.io/openai-agents-python/)
- [MCP SDK Docs](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI ChatKit Docs](https://platform.openai.com/docs/chatkit)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon PostgreSQL Docs](https://neon.tech/docs)

---

**Quickstart Complete**: Your development environment is ready. Begin with `/sp.tasks` to generate implementation tasks.
