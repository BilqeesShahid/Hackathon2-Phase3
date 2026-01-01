# Project Overview — Phase II

## Project Name
The Evolution of Todo

## Phase
Phase II — Full-Stack Web Application

## Purpose
Transform the Phase I in-memory console Todo application into a **secure, multi-user, full-stack web application** with persistent storage and authentication.

## Key Goals
- Support multiple authenticated users
- Persist tasks in a database
- Provide a responsive web interface
- Expose a secure RESTful API
- Enforce strict user data isolation

## Out of Scope
- AI chatbot features (Phase III)
- Kubernetes or cloud-native deployment (Phase IV+)
- Advanced Todo features (recurring tasks, reminders, categories)

## Technology Stack

### Frontend
- Next.js 16+ (App Router)
- TypeScript
- Better Auth for authentication

### Backend
- Python FastAPI
- SQLModel ORM
- RESTful API design

### Database
- Neon Serverless PostgreSQL
- Persistent task storage

---

## Acceptance Criteria

### JWT Issuance
- JWT is issued on successful login
- JWT contains user identifier
- JWT has an expiration time

### API Authorization
- All API requests require a valid JWT
- Requests without JWT return 401 Unauthorized
- Invalid or expired JWTs are rejected

### User Isolation
- Backend extracts user identity from JWT
- All database queries are filtered by user ID
- Cross-user access returns 403 Forbidden

### CRUD Operations
- Users can create tasks with title and optional description
- Users can view only their own tasks
- Users can update their own tasks
- Users can delete their own tasks
- Users can toggle task completion status

---

## User Stories

| As a | I want to | So that |
|------|-----------|---------|
| User | Sign up and sign in | I can have a private task list |
| User | Create tasks | I can track things I need to do |
| User | View my tasks | I can see what I need to accomplish |
| User | Edit tasks | I can update task details |
| User | Delete tasks | I can remove completed or unwanted tasks |
| User | Mark tasks complete | I can track my progress |

---

**Last Updated**: 2025-12-25
