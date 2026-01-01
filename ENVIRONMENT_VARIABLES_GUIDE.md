# 🔐 Environment Variables Guide

## Quick Answer: Where Do Environment Variables Go?

---

## 📍 Variable Placement

### FRONTEND Environment Variables
**Location**: Frontend Vercel Project Settings

```env
BETTER_AUTH_SECRET=<your-secret>
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

### BACKEND Environment Variables
**Location**: Backend Vercel Project Settings

```env
BETTER_AUTH_SECRET=<same-secret-as-frontend>
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.vercel.app
```

---

## 🎯 Detailed Breakdown

### 1. BETTER_AUTH_SECRET

**What**: Secret key for JWT token signing
**Where**: BOTH frontend AND backend
**Value**: MUST be identical in both
**Generate**: `openssl rand -base64 32`

```bash
# Generate it once:
openssl rand -base64 32
# Output example: 8f7e3d2c1b9a0f6e5d4c3b2a1f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e

# Add to BOTH frontend AND backend
```

**Why both?**
- Frontend: Validates JWT tokens
- Backend: Signs JWT tokens
- They must match or authentication breaks!

---

### 2. NEXT_PUBLIC_API_URL

**What**: Backend API endpoint URL
**Where**: FRONTEND only
**Value**: Your backend Vercel URL
**Example**: `https://your-backend.vercel.app`

**Why NEXT_PUBLIC_?**
- Next.js exposes variables starting with `NEXT_PUBLIC_` to the browser
- Frontend JavaScript needs this to make API calls
- Without it, frontend can't reach backend

**Important**: Update this AFTER deploying backend!

---

### 3. DATABASE_URL

**What**: PostgreSQL connection string
**Where**: BACKEND only
**Value**: Your Neon database URL
**Format**: `postgresql://user:password@host:port/database?sslmode=require`

**Example**:
```
postgresql://neonuser:xyz123@ep-cool-snowflake-123456.us-east-1.aws.neon.tech/todoapp?sslmode=require
```

**Where to get it?**
1. Go to https://console.neon.tech
2. Select your project
3. Copy connection string
4. Make sure it includes `?sslmode=require`

**Security**:
- ✅ Backend only (server-side)
- ❌ NEVER in frontend (would expose credentials)

---

### 4. ENVIRONMENT

**What**: Deployment environment
**Where**: BACKEND only
**Value**: `production` for Vercel, `development` for local

**Why?**
- Controls CORS settings
- In production: Allows all Vercel domains
- In development: Allows localhost only

---

### 5. FRONTEND_URL (Optional but Recommended)

**What**: Frontend application URL
**Where**: BACKEND only
**Value**: Your frontend Vercel URL
**Example**: `https://your-frontend.vercel.app`

**Why?**
- For CORS configuration
- Allows backend to know which frontend to trust
- Can be used for redirect URLs

---

## 📊 Visual Guide

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND PROJECT                      │
│                  (Next.js on Vercel)                     │
├─────────────────────────────────────────────────────────┤
│  Environment Variables:                                 │
│  ✓ BETTER_AUTH_SECRET      (shared with backend)       │
│  ✓ NEXT_PUBLIC_API_URL     (points to backend)         │
└─────────────────────────────────────────────────────────┘
                           │
                           │ API Calls
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    BACKEND PROJECT                       │
│                (FastAPI on Vercel)                       │
├─────────────────────────────────────────────────────────┤
│  Environment Variables:                                 │
│  ✓ BETTER_AUTH_SECRET      (shared with frontend)      │
│  ✓ DATABASE_URL            (Neon PostgreSQL)           │
│  ✓ ENVIRONMENT             (production)                │
│  ✓ FRONTEND_URL            (your frontend URL)         │
└─────────────────────────────────────────────────────────┘
                           │
                           │ Database Queries
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    NEON DATABASE                         │
│                  (PostgreSQL Cloud)                      │
└─────────────────────────────────────────────────────────┘
```

---

## ⚡ How to Add Variables in Vercel

### Method 1: During Initial Deploy
1. When creating project, scroll to **Environment Variables**
2. Add each variable name and value
3. Select environments (Production, Preview, Development)
4. Click **Add**
5. Repeat for each variable

### Method 2: After Deployment
1. Go to project in Vercel Dashboard
2. Click **Settings** tab
3. Click **Environment Variables** in sidebar
4. Click **Add New**
5. Enter name and value
6. Select environments
7. Click **Save**
8. **Important**: Redeploy for changes to take effect!

---

## 🔄 When to Redeploy

You MUST redeploy after:
- ✅ Adding new environment variables
- ✅ Changing existing variables
- ✅ Updating backend URL in frontend

**How to Redeploy:**
1. Go to **Deployments** tab
2. Find latest deployment
3. Click **⋯** (three dots)
4. Click **Redeploy**
5. Wait for completion

---

## 🛡️ Security Best Practices

### ✅ DO:
- Keep secrets in environment variables
- Use strong random strings for `BETTER_AUTH_SECRET`
- Use different secrets for dev/staging/production
- Rotate secrets periodically
- Add variables to all environments for consistency

### ❌ DON'T:
- Hardcode secrets in code
- Commit `.env` files to git
- Share secrets in public channels
- Use weak or predictable secrets
- Expose backend variables to frontend

---

## 📋 Checklist Before Deploying

### Frontend Variables:
- [ ] `BETTER_AUTH_SECRET` added
- [ ] `NEXT_PUBLIC_API_URL` added (will update after backend deploy)

### Backend Variables:
- [ ] `BETTER_AUTH_SECRET` added (same as frontend)
- [ ] `DATABASE_URL` added
- [ ] `ENVIRONMENT` set to `production`
- [ ] `FRONTEND_URL` added (optional)

### Verification:
- [ ] All variables added to all environments
- [ ] Secrets are strong and random
- [ ] Database URL is correct
- [ ] URLs don't have trailing slashes
- [ ] Ready to deploy!

---

## 🎓 Understanding Next.js Environment Variables

### Client-side (Browser):
**Prefix**: `NEXT_PUBLIC_*`
**Example**: `NEXT_PUBLIC_API_URL`
**Access**: Available in browser JavaScript
**Use for**: API endpoints, public configuration

```javascript
// Frontend code can access:
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Server-side (Node.js):
**Prefix**: No prefix needed
**Example**: `BETTER_AUTH_SECRET`
**Access**: Server-side code only
**Use for**: Secrets, private config

```javascript
// Server-side code can access:
const secret = process.env.BETTER_AUTH_SECRET;
```

---

## 🐛 Troubleshooting

### Variables Not Working?
1. **Check spelling**: Variable names are case-sensitive
2. **Check deployment**: Did you redeploy after adding?
3. **Check environment**: Added to correct environment?
4. **Check logs**: Look for errors in Vercel logs
5. **Check code**: Using correct variable name?

### Frontend Can't Reach Backend?
- Check `NEXT_PUBLIC_API_URL` is correct
- No trailing slash in URL
- Backend URL is accessible
- CORS is configured correctly

### Authentication Failing?
- `BETTER_AUTH_SECRET` must be IDENTICAL in both
- Check for extra spaces or characters
- Regenerate if uncertain

---

## 📱 Example: Complete Setup

### 1. Generate Secret
```bash
openssl rand -base64 32
# Output: K7j9m2nP8qR3sT5vX6wY1zA4bC7dE9fG2hJ4kL8mN5oP
```

### 2. Frontend Variables
```env
BETTER_AUTH_SECRET=K7j9m2nP8qR3sT5vX6wY1zA4bC7dE9fG2hJ4kL8mN5oP
NEXT_PUBLIC_API_URL=https://todo-backend-xyz.vercel.app
```

### 3. Backend Variables
```env
BETTER_AUTH_SECRET=K7j9m2nP8qR3sT5vX6wY1zA4bC7dE9fG2hJ4kL8mN5oP
DATABASE_URL=postgresql://user:pass@ep-xyz.neon.tech/db?sslmode=require
ENVIRONMENT=production
FRONTEND_URL=https://todo-frontend-abc.vercel.app
```

---

**Made with ❤️ by Bilqees Shahid**
