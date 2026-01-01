# Task CRUD Features — Phase II

## Overview
All task operations require authentication and are scoped to the authenticated user.

## Feature: Create Task

### User Story
As a user, I want to create a new task with a title and optional description.

### API Endpoint
`POST /api/{user_id}/tasks`

### Request Body
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

### Success Response (201 Created)
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": false,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Error Responses
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Attempting to create for another user
- 422 Unprocessable Entity - Validation error

---

## Feature: List Tasks

### User Story
As a user, I want to see all my tasks.

### API Endpoint
`GET /api/{user_id}/tasks`

### Success Response (200 OK)
```json
[
  {
    "id": "integer",
    "user_id": "string",
    "title": "string",
    "description": "string | null",
    "completed": false,
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```

### Error Responses
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Requesting another user's tasks

---

## Feature: Get Task

### User Story
As a user, I want to view details of a specific task.

### API Endpoint
`GET /api/{user_id}/tasks/{id}`

### Success Response (200 OK)
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": false,
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Error Responses
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Accessing another user's task
- 404 Not Found - Task does not exist

---

## Feature: Update Task

### User Story
As a user, I want to edit my task's title or description.

### API Endpoint
`PUT /api/{user_id}/tasks/{id}`

### Request Body
```json
{
  "title": "string (optional, 1-200 chars)",
  "description": "string (optional, max 1000 chars)"
}
```

### Success Response (200 OK)
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Error Responses
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Updating another user's task
- 404 Not Found - Task does not exist

---

## Feature: Delete Task

### User Story
As a user, I want to delete a task.

### API Endpoint
`DELETE /api/{user_id}/tasks/{id}`

### Success Response (204 No Content)

### Error Responses
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Deleting another user's task
- 404 Not Found - Task does not exist

---

## Feature: Toggle Complete

### User Story
As a user, I want to mark a task as complete or incomplete.

### API Endpoint
`PATCH /api/{user_id}/tasks/{id}/complete`

### Success Response (200 OK)
```json
{
  "id": "integer",
  "user_id": "string",
  "title": "string",
  "description": "string | null",
  "completed": "boolean",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Error Responses
- 401 Unauthorized - Missing/invalid JWT
- 403 Forbidden - Modifying another user's task
- 404 Not Found - Task does not exist

---

**Last Updated**: 2025-12-25
