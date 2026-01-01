---
description: "Task list for Phase II Full-Stack Todo Application"
---

# Tasks: Phase II Full-Stack Todo Application

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/openapi.yaml

**Tests**: Tests are NOT included - implementation-only

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- Monorepo structure per plan.md: `src/frontend/`, `src/backend/`
- Backend: `src/backend/app/`
- Frontend: `src/frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create monorepo structure per plan.md (src/frontend/, src/backend/)
- [ ] T002 Create .env.example with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL
- [ ] T003 Initialize Next.js 16+ frontend in src/frontend/ with TypeScript
- [ ] T004 Initialize FastAPI backend in src/backend/ with Python 3.13+
- [ ] T005 [P] Install frontend dependencies: better-auth, axios, react, next
- [ ] T006 [P] Install backend dependencies: fastapi, uvicorn, sqlmodel, pydantic, python-jose, python-multipart

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T007 Create database configuration in src/backend/app/db/config.py
- [ ] T008 Implement SQLModel User model in src/backend/app/models/user.py
- [ ] T009 Implement SQLModel Task model in src/backend/app/models/task.py
- [ ] T010 Create database tables and engine initialization in src/backend/app/db/init.py
- [ ] T011 [P] Implement JWT authentication middleware in src/backend/app/middleware/auth.py
- [ ] T012 [P] Configure CORS middleware in src/backend/app/middleware/cors.py for localhost:3000

### Frontend Foundation

- [ ] T013 Configure Better Auth with JWT plugin in src/frontend/lib/auth.ts
- [ ] T014 Create API client utility with auth in src/frontend/lib/api.ts
- [ ] T015 Create TypeScript types for Task in src/frontend/types/task.ts

### Environment and Config

- [ ] T016 Create .env file from .env.example with actual values
- [ ] T017 Verify JWT secret consistency between frontend and backend

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Authentication (Priority: P1) MVP

**Goal**: Users can sign up and sign in to access their private task list

**Independent Test**: Navigate to /sign-up, create account, sign in, verify redirected to dashboard with user context

### Backend - Authentication

- [ ] T018 [US1] Create auth schemas in src/backend/app/schemas/auth.py (sign up/in request/response)
- [ ] T019 [US1] Create auth router in src/backend/app/routers/auth.py for token validation endpoint

### Frontend - Authentication

- [ ] T020 [US1] Create Sign Up page in src/frontend/app/sign-up/page.tsx
- [ ] T021 [US1] Create Sign In page in src/frontend/app/sign-in/page.tsx
- [ ] T022 [US1] Implement auth context provider in src/frontend/lib/auth-context.tsx
- [ ] T023 [US1] Create auth guard middleware in src/frontend/middleware/auth.ts

**Checkpoint**: User Story 1 complete - users can authenticate

---

## Phase 4: User Story 2 - Create Tasks (Priority: P1) MVP

**Goal**: Users can create tasks with title and optional description

**Independent Test**: Sign in, enter task title "Buy groceries", optional description, click add, verify task appears in list

### Backend - Task Creation

- [ ] T024 [US2] Create task schemas in src/backend/app/schemas/task.py (TaskCreate, TaskResponse)
- [ ] T025 [US2] Implement TaskService in src/backend/app/services/task_service.py (create method)
- [ ] T026 [US2] Create tasks router with POST endpoint in src/backend/app/routers/tasks.py

### Frontend - Task Creation

- [ ] T027 [US2] Create TaskForm component in src/frontend/components/TaskForm.tsx
- [ ] T028 [US2] Implement create task API call in src/frontend/lib/api.ts (createTask function)
- [ ] T029 [US2] Add TaskForm to dashboard page in src/frontend/app/page.tsx

**Checkpoint**: User Stories 1 AND 2 complete - authenticated users can create tasks

---

## Phase 5: User Story 3 - View Tasks (Priority: P1) MVP

**Goal**: Users can view all their tasks in a responsive list

**Independent Test**: Sign in, verify tasks created in US2 appear in list, check for empty state when no tasks

### Backend - Task Listing

- [ ] T030 [US3] Add list tasks endpoint (GET /api/{user_id}/tasks) in src/backend/app/routers/tasks.py
- [ ] T031 [US3] Ensure user isolation in all task queries (filter by user_id from JWT)

### Frontend - Task Display

- [ ] T032 [US3] Create TaskList component in src/frontend/components/TaskList.tsx
- [ ] T033 [US3] Create TaskItem component in src/frontend/components/TaskItem.tsx
- [ ] T034 [US3] Implement list tasks API call in src/frontend/lib/api.ts (getTasks function)
- [ ] T035 [US3] Display task list on dashboard in src/frontend/app/page.tsx

**Checkpoint**: User Stories 1, 2, AND 3 complete - core CRUD MVP ready!

---

## Phase 6: User Story 4 - Edit Tasks (Priority: P2)

**Goal**: Users can edit task title and description

**Independent Test**: Click edit on a task, change title, save, verify change reflects in list

### Backend - Task Update

- [ ] T036 [US4] Add TaskUpdate schema in src/backend/app/schemas/task.py
- [ ] T037 [US4] Implement update method in TaskService in src/backend/app/services/task_service.py
- [ ] T038 [US4] Add PUT endpoint for task update in src/backend/app/routers/tasks.py

### Frontend - Task Editing

- [ ] T039 [US4] Create EditTaskModal component in src/frontend/components/EditTaskModal.tsx
- [ ] T040 [US4] Implement update task API call in src/frontend/lib/api.ts (updateTask function)
- [ ] T041 [US4] Connect edit button in TaskItem to modal in src/frontend/components/TaskItem.tsx

**Checkpoint**: User Story 4 complete - users can edit tasks

---

## Phase 7: User Story 5 - Delete Tasks (Priority: P2)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Click delete on a task, confirm, verify task removed from list

### Backend - Task Deletion

- [ ] T042 [US5] Implement delete method in TaskService in src/backend/app/services/task_service.py
- [ ] T043 [US5] Add DELETE endpoint for task deletion in src/backend/app/routers/tasks.py

### Frontend - Task Deletion

- [ ] T044 [US5] Implement delete task API call in src/frontend/lib/api.ts (deleteTask function)
- [ ] T045 [US5] Add delete confirmation UI in TaskItem component in src/frontend/components/TaskItem.tsx

**Checkpoint**: User Story 5 complete - users can delete tasks

---

## Phase 8: User Story 6 - Toggle Complete (Priority: P2)

**Goal**: Users can mark tasks complete or incomplete to track progress

**Independent Test**: Click checkbox on task, verify strikethrough and status change, click again to undo

### Backend - Completion Toggle

- [ ] T046 [US6] Add TaskToggleComplete schema in src/backend/app/schemas/task.py
- [ ] T047 [US6] Implement toggle_complete method in TaskService in src/backend/app/services/task_service.py
- [ ] T048 [US6] Add PATCH endpoint for completion toggle in src/backend/app/routers/tasks.py

### Frontend - Completion Toggle

- [ ] T049 [US6] Implement toggle complete API call in src/frontend/lib/api.ts (toggleComplete function)
- [ ] T050 [US6] Add completion checkbox to TaskItem component in src/frontend/components/TaskItem.tsx

**Checkpoint**: User Story 6 complete - all CRUD operations working

---

## Phase 9: Polish and Cross-Cutting Concerns

**Purpose**: Improvements that ensure all success criteria are met

### UI/UX Improvements

- [ ] T051 [P] Add loading states during API calls in components
- [ ] T052 [P] Add error handling and toast notifications for API errors
- [ ] T053 [P] Add responsive design for mobile devices
- [ ] T054 [P] Add empty state UI when no tasks exist

### Backend Polish

- [ ] T055 Add health check endpoint GET /health in src/backend/app/routers/health.py
- [ ] T056 Add request validation and proper error responses
- [ ] T057 Add logging for all API operations

### Final Validation

- [ ] T058 Run quickstart.md validation - verify full auth plus CRUD flow
- [ ] T059 Verify user isolation - test accessing another user task returns 403
- [ ] T060 Verify JWT required on all endpoints - test without token returns 401

---

## Dependencies and Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|------------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories |
| Phase 3: US1 (Auth) | Phase 2 | US2, US3, US4, US5, US6 |
| Phase 4: US2 (Create) | Phase 2, US1 | - |
| Phase 5: US3 (View) | Phase 2, US1 | - |
| Phase 6: US4 (Edit) | Phase 2, US1, US3 | - |
| Phase 7: US5 (Delete) | Phase 2, US1, US3 | - |
| Phase 8: US6 (Complete) | Phase 2, US1, US3 | - |
| Phase 9: Polish | All Phases 1-8 | - |

### User Story Dependencies

- **User Story 1 (Auth)**: Foundation prerequisite - Authentication block
- **User Stories 2-6**: All require Foundation plus Auth complete
- All stories independently testable once their prerequisites are met

### Parallel Opportunities

- Phase 1 tasks marked [P] can run in parallel
- Phase 2 tasks marked [P] can run in parallel (within Phase 2)
- Once Foundation is done, User Stories 2-6 can proceed in parallel
- Within each story, model/schema tasks marked [P] can parallelize

---

## Parallel Execution Examples

### After Foundation Complete

```
Developer A: User Story 2 (Create)
- Create task schemas in src/backend/app/schemas/task.py
- Implement TaskService.create method in src/backend/app/services/task_service.py
- Create TaskForm component in src/frontend/components/TaskForm.tsx

Developer B: User Story 3 (View)
- Add list tasks endpoint in src/backend/app/routers/tasks.py
- Create TaskList component in src/frontend/components/TaskList.tsx
- Create TaskItem component in src/frontend/components/TaskItem.tsx

Developer C: User Stories 4-6 (Edit, Delete, Toggle)
- Add TaskUpdate schema and update endpoint
- Add delete endpoint and UI
- Add toggle complete endpoint and checkbox
```

---

## Implementation Strategy

### MVP First (Auth plus Create plus View)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (Create)
5. Complete Phase 5: User Story 3 (View)
6. STOP and VALIDATE: Sign up, sign in, create task, view task
7. Demo if ready

### Incremental Delivery

1. Complete Setup plus Foundational -> Foundation ready
2. Add US1 (Auth) -> Users can sign in
3. Add US2 (Create) -> Users can add tasks -> **MVP!**
4. Add US3 (View) -> Users see their tasks
5. Add US4 (Edit) -> Users can modify tasks
6. Add US5 (Delete) -> Users can remove tasks
7. Add US6 (Complete) -> Users can track progress
8. Polish -> Final delivery

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup plus Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Auth)
   - Developer B: User Stories 2-3 (Create plus View)
   - Developer C: User Stories 4-6 (Edit plus Delete plus Toggle)
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 6 | Project structure, dependencies |
| Phase 2: Foundational | 12 | DB, Auth, CORS, API client, Types |
| Phase 3: US1 (Auth) | 6 | Sign up/in, auth guard |
| Phase 4: US2 (Create) | 6 | Task creation |
| Phase 5: US3 (View) | 6 | Task listing |
| Phase 6: US4 (Edit) | 6 | Task editing |
| Phase 7: US5 (Delete) | 4 | Task deletion |
| Phase 8: US6 (Complete) | 5 | Completion toggle |
| Phase 9: Polish | 10 | UI, validation, testing |
| **Total** | **61** | |

**MVP Scope**: Phases 1-5 (User Stories 1-3) - Auth plus Create plus View tasks

**Parallel Opportunities**: 15 tasks marked [P] across all phases

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Verify user isolation by testing 403 Forbidden on cross-user access
- Verify JWT required by testing 401 Unauthorized without token
