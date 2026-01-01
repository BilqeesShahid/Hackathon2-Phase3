# REST API Specification — Phase II

## Base URL
`/api`

## Authentication
All endpoints require:
```
Authorization: Bearer <JWT>
```

---

## Endpoints

### GET /api/{user_id}/tasks
List all tasks for authenticated user.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |

**Response**: 200 OK - Array of task objects

---

### POST /api/{user_id}/tasks
Create a new task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |

**Request Body**:
```json
{
  "title": "string",
  "description": "string (optional)"
}
```

**Response**: 201 Created - Created task object

---

### GET /api/{user_id}/tasks/{id}
Get task details.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |
| `id` | integer | Task ID |

**Response**: 200 OK - Task object

---

### PUT /api/{user_id}/tasks/{id}
Update task title or description.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |
| `id` | integer | Task ID |

**Request Body**:
```json
{
  "title": "string (optional)",
  "description": "string (optional)"
}
```

**Response**: 200 OK - Updated task object

---

### DELETE /api/{user_id}/tasks/{id}
Delete a task.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |
| `id` | integer | Task ID |

**Response**: 204 No Content

---

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status.

| Parameter | Type | Description |
|-----------|------|-------------|
| `user_id` | string | User ID from JWT claims |
| `id` | integer | Task ID |

**Response**: 200 OK - Updated task object

---

## Error Handling

| Status | Condition |
|--------|-----------|
| 401 Unauthorized | Missing or invalid JWT token |
| 403 Forbidden | Accessing another user's task |
| 404 Not Found | Task does not exist |
| 422 Unprocessable Entity | Validation error |

---

**Last Updated**: 2025-12-25
