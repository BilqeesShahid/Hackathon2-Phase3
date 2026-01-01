# 🚀 Vercel Deployment Guide

Complete guide to deploy your Todo Application frontend and backend separately on Vercel.

---

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Git Repository**: Your code pushed to GitHub/GitLab/Bitbucket
3. **Neon Database**: PostgreSQL database URL ready
4. **Better Auth Secret**: Generate using: `openssl rand -base64 32`

---

## 🎨 PART 1: Deploy Frontend (Next.js)

### Step 1: Create Frontend Project on Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..." → Project**
3. Import your Git repository
4. Configure project settings:
   - **Framework Preset**: Next.js
   - **Root Directory**: `src/frontend`
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)
   - **Install Command**: `npm install` (default)

### Step 2: Add Frontend Environment Variables

In Vercel project settings → **Environment Variables**, add:

```env
BETTER_AUTH_SECRET=your-generated-secret-here
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

**Important Notes:**
- `BETTER_AUTH_SECRET`: Same secret for both frontend and backend
- `NEXT_PUBLIC_API_URL`: Your backend URL (you'll get this after deploying backend)
- Variables starting with `NEXT_PUBLIC_` are exposed to the browser
- Set these for **Production**, **Preview**, and **Development** environments

### Step 3: Deploy Frontend

1. Click **"Deploy"**
2. Wait for build to complete
3. Note your frontend URL: `https://your-app.vercel.app`

---

## ⚙️ PART 2: Deploy Backend (Python FastAPI)

### Step 1: Create Backend Project on Vercel

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click **"Add New..." → Project**
3. Import the SAME Git repository (separate project)
4. Configure project settings:
   - **Framework Preset**: Other
   - **Root Directory**: `src/backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Output Directory**: Leave empty
   - **Install Command**: Leave empty

### Step 2: Add Backend Environment Variables

In Vercel project settings → **Environment Variables**, add:

```env
BETTER_AUTH_SECRET=your-generated-secret-here
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/phase2?sslmode=require
ENVIRONMENT=production
```

**Important Notes:**
- `BETTER_AUTH_SECRET`: MUST be the same as frontend
- `DATABASE_URL`: Your Neon PostgreSQL connection string
- `ENVIRONMENT`: Set to `production` for production deployment
- These variables are SERVER-SIDE ONLY (not exposed to browser)
- Set for **Production**, **Preview**, and **Development** environments

### Step 3: Deploy Backend

1. Click **"Deploy"**
2. Wait for build to complete
3. Note your backend URL: `https://your-backend.vercel.app`

### Step 4: Update Frontend with Backend URL

1. Go to your **frontend** Vercel project
2. Navigate to **Settings → Environment Variables**
3. Update `NEXT_PUBLIC_API_URL` with your actual backend URL:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
   ```
4. **Redeploy** the frontend to apply changes

---

## 🔐 Environment Variables Summary

### Frontend Environment Variables
```env
BETTER_AUTH_SECRET=<same-secret-as-backend>
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

### Backend Environment Variables
```env
BETTER_AUTH_SECRET=<same-secret-as-frontend>
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
ENVIRONMENT=production
```

---

## 📁 Configuration Files

The following configuration files have been created for you:

### Frontend: `src/frontend/vercel.json`
- Configures Next.js deployment
- Sets up routing and redirects

### Backend: `src/backend/vercel.json`
- Configures Python runtime
- Sets up FastAPI serverless functions
- Handles CORS and API routes

---

## ✅ Post-Deployment Checklist

- [ ] Frontend deploys successfully
- [ ] Backend deploys successfully
- [ ] Database connection works (check backend logs)
- [ ] Frontend can call backend API
- [ ] User registration works
- [ ] User login works
- [ ] Task CRUD operations work
- [ ] CORS is properly configured

---

## 🔧 Common Issues & Solutions

### Issue 1: CORS Errors
**Solution**: Ensure your backend's CORS settings allow your frontend domain:
```python
# In main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 2: Environment Variables Not Working
**Solution**:
- Make sure variables are set for the correct environment
- Redeploy after adding/changing variables
- Check variable names are exact (case-sensitive)

### Issue 3: Backend Not Found (404)
**Solution**: Check `vercel.json` configuration and ensure API routes match

### Issue 4: Database Connection Fails
**Solution**:
- Verify DATABASE_URL is correct
- Ensure Neon database allows connections
- Check database exists and is accessible

### Issue 5: Authentication Fails
**Solution**:
- Verify `BETTER_AUTH_SECRET` is IDENTICAL in both frontend and backend
- Check token generation and validation logic

---

## 📱 Testing Your Deployment

1. Open your frontend URL
2. Create a new account
3. Sign in
4. Create a task
5. Update a task
6. Delete a task
7. Sign out

---

## 🔄 Redeployment

Vercel automatically redeploys on git push:
- Push to main branch → Production deployment
- Push to other branches → Preview deployment

Manual redeploy:
1. Go to Vercel dashboard
2. Select your project
3. Go to **Deployments** tab
4. Click **"Redeploy"** on any deployment

---

## 📊 Monitoring

- **Vercel Dashboard**: View logs, analytics, and performance
- **Runtime Logs**: Check for errors in deployment logs
- **Analytics**: Monitor user traffic and performance

---

## 🆘 Need Help?

- Vercel Documentation: https://vercel.com/docs
- FastAPI on Vercel: https://vercel.com/docs/frameworks/python
- Next.js on Vercel: https://vercel.com/docs/frameworks/nextjs

---

**Made with ❤️ by Bilqees Shahid**
