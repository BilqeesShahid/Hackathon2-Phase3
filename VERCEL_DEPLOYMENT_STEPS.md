# 🚀 Quick Vercel Deployment Steps

## Step-by-Step Guide for Deploying Frontend & Backend

---

## 🎯 Before You Start

### 1. Generate Better Auth Secret
```bash
openssl rand -base64 32
```
**Copy this secret** - you'll need it for both frontend and backend!

### 2. Get Your Database URL
Make sure you have your Neon PostgreSQL connection string ready:
```
postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/database?sslmode=require
```

---

## 🎨 FRONTEND DEPLOYMENT

### Step 1: Create Frontend Project
1. Go to https://vercel.com/new
2. Import your repository
3. Configure:
   - **Root Directory**: `src/frontend`
   - **Framework**: Next.js (auto-detected)
   - **Build Command**: `npm run build`
   - **Install Command**: `npm install`

### Step 2: Add Environment Variables
Click **Environment Variables** and add:

| Variable Name | Value | Where to Add |
|--------------|-------|--------------|
| `BETTER_AUTH_SECRET` | Your generated secret | All environments |
| `NEXT_PUBLIC_API_URL` | `https://your-backend.vercel.app` | All environments |

**Note**: You'll update `NEXT_PUBLIC_API_URL` after deploying backend

### Step 3: Deploy
1. Click **Deploy**
2. Wait for deployment
3. **Copy your frontend URL**: `https://your-frontend.vercel.app`

---

## ⚙️ BACKEND DEPLOYMENT

### Step 1: Create Backend Project
1. Go to https://vercel.com/new
2. Import the **SAME repository**
3. Configure:
   - **Root Directory**: `src/backend`
   - **Framework**: Other
   - Leave other fields as default

### Step 2: Add Environment Variables
Click **Environment Variables** and add:

| Variable Name | Value | Where to Add |
|--------------|-------|--------------|
| `BETTER_AUTH_SECRET` | Same secret as frontend | All environments |
| `DATABASE_URL` | Your Neon PostgreSQL URL | All environments |
| `ENVIRONMENT` | `production` | Production only |
| `FRONTEND_URL` | Your frontend URL from Step 3 above | All environments |

### Step 3: Deploy
1. Click **Deploy**
2. Wait for deployment
3. **Copy your backend URL**: `https://your-backend.vercel.app`

---

## 🔄 FINAL STEP: Update Frontend

### Update Backend URL in Frontend
1. Go to your **frontend** project on Vercel
2. Settings → Environment Variables
3. **Edit** `NEXT_PUBLIC_API_URL`:
   ```
   NEXT_PUBLIC_API_URL=https://your-actual-backend-url.vercel.app
   ```
4. Click **Save**
5. Go to **Deployments** tab
6. Click **"Redeploy"** button on the latest deployment
7. Wait for redeployment to complete

---

## ✅ Testing Your Deployment

1. Open your frontend URL: `https://your-frontend.vercel.app`
2. Click "Create Account"
3. Register a new user
4. Sign in
5. Create a task
6. Update the task
7. Delete the task
8. Sign out

If all steps work → **Deployment Successful!** 🎉

---

## 🔍 Environment Variables Summary

### Frontend (.env)
```env
BETTER_AUTH_SECRET=abc123...xyz
NEXT_PUBLIC_API_URL=https://your-backend.vercel.app
```

### Backend (.env)
```env
BETTER_AUTH_SECRET=abc123...xyz
DATABASE_URL=postgresql://user:password@host/db?sslmode=require
ENVIRONMENT=production
FRONTEND_URL=https://your-frontend.vercel.app
```

**CRITICAL**: `BETTER_AUTH_SECRET` must be **identical** in both!

---

## ⚠️ Common Issues

### Issue 1: "Network Error" when signing in
**Cause**: Backend URL not set correctly in frontend
**Fix**: Update `NEXT_PUBLIC_API_URL` and redeploy frontend

### Issue 2: CORS errors in browser console
**Cause**: Frontend URL not whitelisted in backend
**Fix**:
1. Check `FRONTEND_URL` is set in backend
2. Update `cors.py` if needed (already done in `cors_production.py`)
3. Redeploy backend

### Issue 3: Authentication fails
**Cause**: Different secrets in frontend/backend
**Fix**: Ensure `BETTER_AUTH_SECRET` is **identical** in both

### Issue 4: Database connection error
**Cause**: Invalid `DATABASE_URL`
**Fix**:
1. Check your Neon dashboard for correct URL
2. Ensure database exists
3. Check connection string format

### Issue 5: Build fails on Vercel
**Frontend Fix**: Check `package.json` scripts
**Backend Fix**: Check `requirements.txt` dependencies

---

## 📊 Where to Add Environment Variables

### In Vercel Dashboard:
1. Select your project
2. Go to **Settings**
3. Click **Environment Variables**
4. Add each variable with these options:
   - **Production**: For live site
   - **Preview**: For PR/branch previews
   - **Development**: For local development

**Pro Tip**: Add to ALL THREE for consistency

---

## 🎯 Deployment Checklist

- [ ] Generated `BETTER_AUTH_SECRET`
- [ ] Got Neon `DATABASE_URL`
- [ ] Deployed Frontend to Vercel
- [ ] Deployed Backend to Vercel
- [ ] Added all environment variables
- [ ] Updated `NEXT_PUBLIC_API_URL` in frontend
- [ ] Redeployed frontend with correct backend URL
- [ ] Tested user registration
- [ ] Tested user login
- [ ] Tested task CRUD operations
- [ ] Checked for console errors
- [ ] Verified CORS is working

---

## 🆘 Need Help?

### Check Vercel Logs:
1. Go to your project in Vercel
2. Click **Deployments**
3. Click on a deployment
4. View **Build Logs** or **Function Logs**

### Check Browser Console:
1. Open your frontend
2. Press `F12` (Developer Tools)
3. Go to **Console** tab
4. Look for errors

---

## 🎉 Success!

Once everything is working:
- ✅ Frontend is live
- ✅ Backend is live
- ✅ Database is connected
- ✅ Users can register and login
- ✅ Tasks can be created, updated, deleted

**Your full-stack app is now deployed!** 🚀

---

**Made with ❤️ by Bilqees Shahid**
