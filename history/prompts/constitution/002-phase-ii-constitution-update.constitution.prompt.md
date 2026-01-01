---
id: "002"
title: "Phase II Constitution Update"
stage: "constitution"
date: "2025-12-25"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-todo-console-app"
user: "user"
command: "/sp.constitution # Constitution — Phase II"
labels: ["constitution","phase-ii","full-stack"]
links:
  spec: "null"
  ticket: "null"
  adr: "null"
  pr: "null"
files:
  - ".specify/memory/constitution.md"
tests:
  - "null"
---

## Prompt

update /sp.constituion  # 📜 Constitution — Phase II
## Todo Full-Stack Web Application
**Hackathon II: Spec-Driven Development**

**Date:** 25 December 2025
**Phase:** II — Full-Stack Web Application
**Project:** The Evolution of Todo

---

## 1. Purpose

This Constitution governs **Phase II** of the *Evolution of Todo* project.
It defines the **non-negotiable principles, constraints, and architectural laws** that guide the transformation of the Phase I console application into a **secure, multi-user, full-stack web application** using **Spec-Driven Development**.

This document exists to ensure:

- Architectural consistency
- Security by design
- AI-native development discipline
- Strict separation of concerns
- Reproducibility through specifications

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

## 3. Scope of Phase II

Phase II converts the Todo application into a **persistent, authenticated, multi-user web system**.

### Included

- Full-stack architecture (Frontend + Backend)
- RESTful API
- Database persistence
- User authentication and isolation
- Responsive web interface

### Excluded

- AI chatbot functionality (Phase III)
- Kubernetes or cloud deployment (Phase IV+)
- Intermediate and advanced features (recurring tasks, reminders, Kafka)

---

## 4. Mandatory Feature Set (Basic Level)

Phase II MUST implement all five **Basic Level** Todo features as a web application:

1. Add Task
2. Delete Task
3. Update Task
4. View Task List
5. Mark Task as Complete

All task operations MUST be:

- Authenticated
- User-scoped
- Persisted in the database

---

## 5. Architecture Laws

### 5.1 Layered Architecture (Required)

The system MUST follow a strict layered architecture:

Frontend (Next.js)
↓
REST API (FastAPI)
↓
ORM Layer (SQLModel)
↓
Database (Neon PostgreSQL)

yaml
Copy code

No layer may bypass another.

---

### 5.2 Monorepo Requirement

Phase II MUST be implemented as a **single monorepo** with:

- Unified Spec-Kit context
- Separate frontend and backend directories
- Shared specifications

This structure is mandatory to allow Claude Code full cross-stack visibility.

---

## 6. Technology Mandates

### 6.1 Frontend

- Next.js 16+ (App Router)
- TypeScript
- Responsive UI design
- Authentication via **Better Auth**

---

### 6.2 Backend

- Python **FastAPI**
- RESTful API endpoints
- Stateless request handling
- JWT verification middleware

---

### 6.3 Database

- **Neon Serverless PostgreSQL**
- **SQLModel ORM**
- Persistent storage for all tasks
- In-memory task storage is forbidden

---

## 7. Authentication & Security Constitution

### 7.1 Authentication Is Mandatory

- All API endpoints MUST require authentication
- Anonymous or public access is prohibited

---

### 7.2 JWT-Based Authorization

- Better Auth MUST issue JWT tokens
- Frontend MUST attach JWT tokens to every API request
- Backend MUST validate JWT tokens on every request
- JWT signing secret MUST be shared via environment variables

---

### 7.3 User Isolation Law

- Users may access ONLY their own tasks
- Cross-user data access is strictly forbidden
- User identity MUST be derived from verified JWT claims
- Ownership MUST be enforced at the database query level

Any violation of user isolation invalidates Phase II.

---

## 8. API Design Rules

- All endpoints MUST be RESTful
- All endpoints MUST live under `/api/`
- All responses MUST be JSON
- HTTP status codes MUST be semantically correct
- Errors MUST return clear, explicit messages

GraphQL, RPC, or non-HTTP APIs are not permitted in Phase II.

---

## 9. Data Integrity Rules

- Every task MUST belong to exactly one user
- Task ownership MUST be enforced on every operation
- Deleting a task MUST NOT affect other users' data
- Task identifiers MUST NOT be guessable across users

---

## 10. Specification Requirements

Phase II MUST include specifications for:

- System architecture
- Task CRUD operations
- Authentication and authorization
- REST API endpoints
- Database schema
- UI structure and behavior

All specifications MUST:

- Be written in Markdown
- Be human-readable
- Be explicitly referenced when invoking Claude Code

---

## 11. Claude Code Usage Law

Claude Code MUST:

- Read relevant specifications before generating code
- Implement both frontend and backend changes when required
- Respect all architectural and security constraints
- Never invent features not defined in specifications

If ambiguity exists, Claude Code MUST stop and request specification clarification.

---

## 12. Required Deliverables (Phase II)

A valid Phase II submission MUST include:

- Public GitHub repository
- Phase II Constitution file
- `/specs` directory with complete specifications
- Working Next.js frontend application
- Working FastAPI backend service
- Neon PostgreSQL database integration
- Authentication implemented with Better Auth
- Root and subproject `CLAUDE.md` files
- README with clear setup instructions

---

## 13. Evaluation Criteria

Phase II submissions are evaluated on:

- Adherence to Spec-Driven Development
- Correct authentication and user isolation
- API correctness and security
- Clean architectural separation
- Specification completeness and clarity
- Proper use of Claude Code without manual coding

---

## 14. Non-Negotiable Rule

> **If it is not specified, it must not be implemented.**
> **If it is incorrect, the specification must be fixed — never the code.**

This Constitution is fin

## Response snapshot

Updated `.specify/memory/constitution.md` from Phase I to Phase II constitution. The new constitution defines:
- Full-stack web application architecture (Next.js + FastAPI + Neon PostgreSQL)
- Better Auth + JWT authentication requirements
- Layered architecture mandates
- User isolation laws
- Technology stack specifications
- Evaluation criteria for Phase II submission

## Outcome

- ✅ Impact: Phase II governing document established with full-stack architecture, authentication mandates, and security constraints
- 🧪 Tests: N/A - constitution update
- 📁 Files: 1 modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create system architecture specification, Define REST API endpoints specification, Create database schema specification, Define UI structure specification
- 🧠 Reflection: Phase II constitution establishes comprehensive framework for full-stack web application with strict security and architectural requirements

## Evaluation notes (flywheel)

- Failure modes observed: "null"
- Graders run and results (PASS/FAIL): "N/A"
- Prompt variant (if applicable): "null"
- Next experiment (smallest change to try): "null"
