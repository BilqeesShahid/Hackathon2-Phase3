# Quickstart Guide: Phase II Full-Stack Todo Application

**Date**: 2025-12-25 | **Feature**: Phase II Full-Stack Todo App

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.13+ | Backend runtime |
| Node.js | 20+ | Frontend runtime |
| pip / uv | Latest | Python package manager |
| npm / pnpm | Latest | Node package manager |
| Git | 2.0+ | Version control |

---

## Environment Setup

### 1. Clone and Enter Directory

```bash
git clone <repository-url>
cd hack2-Phase2
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env
```

**Required variables**:

```bash
# Shared JWT secret (generate a strong random string)
BETTER_AUTH_SECRET=your-256-bit-secret-key-min-32-chars

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend (Neon PostgreSQL connection)
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/phase2?sslmode=require
```

**Generate a secure secret**:

```bash
# Linux/macOS
openssl rand -base64 32

# Windows (PowerShell)
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Min 0 -Max 255 }))
```

---

## Backend Setup (FastAPI)

### 1. Navigate to Backend

```bash
cd src/backend
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate   # Windows

# Or using uv (faster)
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

**requirements.txt**:
```
fastapi>=0.109.0
uvicorn>=0.27.0
sqlmodel>=0.0.14
pydantic>=2.5.0
python-jose[cryptography]>=3.3.0
python-multipart>=0.0.6
neon==0.1.0  # or psycopg2-binary
python-dotenv>=1.0.0
```

### 4. Initialize Database

```bash
# Create tables from SQLModel
python -c "from app.models import create_db; create_db()"
```

Or run migrations if using Alembic (future enhancement):

```bash
alembic upgrade head
```

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### 6. Verify Backend Health

```bash
curl http://localhost:8000/health
```

**Response**:
```json
{"status": "healthy", "version": "1.0.0"}
```

---

## Frontend Setup (Next.js)

### 1. Navigate to Frontend

```bash
cd src/frontend
```

### 2. Install Dependencies

```bash
npm install
# or
pnpm install
```

**Key dependencies** (package.json):
```json
{
  "dependencies": {
    "next": "14.x",
    "react": "^18",
    "react-dom": "^18",
    "better-auth": "latest",
    "axios": "^1.6.0"
  }
}
```

### 3. Start Development Server

```bash
npm run dev
# or
pnpm dev
```

**Expected output**:
```
Ready on http://localhost:3000
```

### 4. Verify Frontend

Open http://localhost:3000 in your browser.

---

## Full Stack Development

### Running Both Services

**Terminal 1 (Backend)**:
```bash
cd src/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend)**:
```bash
cd src/frontend
npm run dev
```

### Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web UI |
| Backend API | http://localhost:8000/api | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Health Check | http://localhost:8000/health | Service status |

---

## Testing the Flow

### 1. Sign Up (via Frontend)

1. Navigate to /sign-up
2. Enter email and password
3. Submit form
4. Check for successful registration

### 2. Create a Task

1. After sign-in, navigate to dashboard
2. Enter task title: "Test task"
3. Optional: Add description
4. Click "Add Task"
5. Verify task appears in list

### 3. Test API Directly

```bash
# Get JWT token from browser DevTools (Application -> Cookies)
TOKEN="your-jwt-token"

# List tasks
curl -X GET http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN"

# Create task
curl -X POST http://localhost:8000/api/{user_id}/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "API test task"}'
```

---

## Troubleshooting

### CORS Errors

If frontend requests fail with CORS errors:

```bash
# Verify backend CORS configuration
curl -I http://localhost:8000/api/health
```

Ensure http://localhost:3000 is in allow_origins in app/main.py.

### JWT Validation Fails

1. Check BETTER_AUTH_SECRET is identical in .env and frontend
2. Verify token has not expired
3. Check token format: Authorization: Bearer <token>

### Database Connection

```bash
# Test Neon connection
python -c "from app.db import engine; print(engine.connect())"
```

Ensure DATABASE_URL has sslmode=require for Neon.

---

## Next Steps

1. Implement backend - Follow specs/api/rest-endpoints.md
2. Implement frontend - Follow specs/ui/pages-and-components.md
3. Write tests - pytest for backend, Jest for frontend
4. Deploy - Vercel (frontend) + Railway/Render (backend)

---

**Quickstart completed**: 2025-12-25
