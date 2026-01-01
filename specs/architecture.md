# System Architecture — Phase II

## Architecture Overview

The system follows a **layered architecture** with clear separation of concerns:

```
┌─────────────────────────────────────┐
│         Frontend (Next.js)          │
│    Pages, Components, Auth UI       │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│        REST API (FastAPI)           │
│    Endpoints, JWT Validation        │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│       ORM Layer (SQLModel)          │
│    Models, Queries, Relationships   │
└─────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│    Database (Neon PostgreSQL)       │
│    Persistent Storage               │
└─────────────────────────────────────┘
```

## Component Responsibilities

### Frontend (Next.js)
- Render UI pages and components
- Manage user authentication state
- Make API calls to backend
- Handle user interactions

### Backend (FastAPI)
- Expose RESTful endpoints
- Validate JWT tokens
- Enforce user isolation
- Process business logic

### ORM Layer (SQLModel)
- Define database models
- Handle database operations
- Enforce relationships and constraints

### Database (Neon PostgreSQL)
- Persist users and tasks
- Enforce referential integrity
- Provide efficient queries

---

## Data Flow

### Authenticated Request Flow
1. User signs in via Better Auth
2. Frontend receives JWT token
3. Frontend attaches JWT to API requests
4. Backend validates JWT and extracts user ID
5. Backend filters all queries by user ID
6. Response returns only user's data

---

## Security Model

### Authentication
- Better Auth manages user credentials
- JWT tokens issued on successful authentication
- Tokens include expiration time

### Authorization
- All API endpoints require valid JWT
- Backend enforces user-task ownership
- Cross-user access is forbidden

### Environment Variables
- `BETTER_AUTH_SECRET` - JWT signing secret
- `DATABASE_URL` - Neon PostgreSQL connection
- `NEXT_PUBLIC_API_URL` - Backend API URL

---

## Directory Structure

```
/specs
  overview.md
  architecture.md
  /features
    task-crud.md
    authentication.md
  /api
    rest-endpoints.md
  /database
    schema.md
  /ui
    pages-and-components.md

/src
  /frontend (Next.js)
    /app
    /components
    /lib
  /backend (FastAPI)
    /app
      /models
      /routers
      /services
```

---

**Last Updated**: 2025-12-25
