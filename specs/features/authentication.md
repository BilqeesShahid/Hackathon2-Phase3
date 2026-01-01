# Authentication Specification — Phase II

## Overview
All API endpoints require JWT-based authentication. User identity is derived from the JWT token claims.

## Authentication Flow

### Sign Up
1. User provides email and password
2. Better Auth creates user account
3. JWT token is issued
4. Frontend stores token securely

### Sign In
1. User provides email and password
2. Better Auth validates credentials
3. JWT token is issued
4. Frontend attaches token to all API requests

### Token Management
- Token includes `user_id` claim
- Token has expiration (e.g., 7 days)
- Frontend includes token in `Authorization: Bearer <token>` header

---

## JWT Claims

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567890
}
```

| Claim | Description |
|-------|-------------|
| `sub` | User identifier (UUID) |
| `email` | User email address |
| `exp` | Token expiration timestamp |
| `iat` | Token issued at timestamp |

---

## Backend Authorization Middleware

### JWT Validation
1. Extract `Authorization` header from request
2. Validate header format: `Bearer <token>`
3. Verify JWT signature using `BETTER_AUTH_SECRET`
4. Check token expiration
5. Extract `user_id` from claims

### User Isolation Enforcement
- All endpoints require `user_id` in path
- Backend validates `user_id` matches JWT claim
- Mismatch returns 403 Forbidden
- All database queries include `WHERE user_id = :uid`

---

## Error Codes

| Code | Condition |
|------|-----------|
| 401 Unauthorized | Missing or malformed Authorization header |
| 401 Unauthorized | Invalid or expired JWT |
| 403 Forbidden | User ID in path doesn't match JWT |

---

## Environment Variables

```bash
BETTER_AUTH_SECRET=<secret-key-for-jwt-signing>
DATABASE_URL=<neon-postgres-connection-string>
```

---

**Last Updated**: 2025-12-25
