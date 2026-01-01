# Research Findings: Phase II Full-Stack Todo Application

**Date**: 2025-12-25 | **Feature**: Phase II Full-Stack Todo App

---

## 1. Better Auth JWT Integration with FastAPI

### Decision
Use Better Auth's JWT plugin with shared HMAC secret for validation in FastAPI.

### Rationale
- Better Auth natively supports JWT tokens via its JWT plugin
- Both frontend and backend can validate tokens using the same secret
- HMAC-SHA256 is the recommended algorithm for JWT signing

### Implementation Pattern

**Frontend (Better Auth config)**:
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  plugins: [
    jwt({
      jwt: {
        secret: process.env.BETTER_AUTH_SECRET,
      },
    }),
  ],
});
```

**Backend (FastAPI middleware)**:
```python
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        return {"user_id": payload["sub"], "email": payload["email"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Alternatives Considered
- **Session-based auth**: Rejected - JWT required by constitution
- **OAuth2/OIDC**: Overkill for this scope, adds complexity

---

## 2. SQLModel + Neon PostgreSQL Best Practices

### Decision
Use SQLModel's async support with Neon serverless driver's pooler connection.

### Rationale
- Neon provides a serverless driver optimized for Vercel/edge functions
- Async SQLModel works well with FastAPI's async endpoints
- Connection pooling prevents exhaustions in serverless environments

### Implementation Pattern

**Database connection**:
```python
from sqlmodel import create_engine, Session, SQLModel
from neon import NeonDatabase

# Use Neon serverless driver
database_url = os.environ["DATABASE_URL"]
engine = create_engine(database_url, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
```

**SQLModel entities**:
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: list["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, autogen=True)
    user_id: str = Field(foreign_key="user.id", on_delete="CASCADE")
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: User = Relationship(back_populates="tasks")
```

### Alternatives Considered
- **SQLAlchemy async**: More complex setup, SQLModel provides cleaner type hints
- **Raw psycopg2**: No type safety, manual connection management

---

## 3. Next.js + FastAPI CORS Configuration

### Decision
Configure CORS to allow credentials with specific origin patterns for development.

### Rationale
- Development: Allow localhost:3000 (Next.js) to access localhost:8000 (FastAPI)
- Production: Restrict to specific domain
- Credentials require `allow_credentials: true` and explicit origin

### Implementation Pattern

**FastAPI CORS**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Next.js API route**:
```typescript
// src/lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchWithAuth<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const session = await auth.getSession();
  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${session?.token}`,
      "Content-Type": "application/json",
    },
    credentials: "include",
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
```

---

## 4. Environment Variable Sharing Strategy

### Decision
Use a root `.env.example` and project-specific `.env` files with shared secrets documented.

### Rationale
- JWT secret must be identical across frontend and backend
- Neon connection string can differ per environment
- Clear documentation prevents mismatched configurations

### Pattern

**Root `.env.example`**:
```bash
# Shared secrets (must be identical)
BETTER_AUTH_SECRET=your-256-bit-secret-key-here

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-1.aws.neon.tech/phase2
```

**Development workflow**:
1. Copy `.env.example` to `.env` in project root
2. Frontend reads from `process.env`
3. Backend reads from `python-dotenv` or Pydantic settings
4. Both use same `BETTER_AUTH_SECRET` for JWT validation

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| JWT Validation | Shared HMAC secret | Simpler than OAuth, matches constitution |
| Database | SQLModel + Neon async | Type safety, serverless-optimized |
| CORS | Explicit localhost origins | Security + dev experience |
| Env vars | Root `.env.example` | Single source of truth for secrets |

---

**Research completed**: 2025-12-25
