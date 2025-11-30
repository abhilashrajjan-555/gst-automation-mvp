# 🚀 Railway Deployment Guide

This guide will help you deploy the GST Automation MVP to Railway.app.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host the code.
2. **Railway Account**: Sign up at [railway.app](https://railway.app).
3. **Supabase Project**: You already have this!

---

## Step 1: Push Code to GitHub

1. Create a new **Private Repository** on GitHub named `gst-automation-mvp`.
2. Push your local code to this repository:

```bash
# Initialize git if you haven't
git init
git add .
git commit -m "Ready for deployment"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/gst-automation-mvp.git
git branch -M main
git push -u origin main
```

---

## Step 2: Create Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard).
2. Click **+ New Project** → **Deploy from GitHub repo**.
3. Select your `gst-automation-mvp` repository.
4. Click **Deploy Now**.

**STOP!** Railway will try to auto-detect the setup. We want to configure it manually for our monorepo (Frontend + Backend).

---

## Step 3: Configure Backend Service

1. In the project view, you'll see a service created from your repo. Click on it.
2. Go to **Settings** → **General**.
3. Change **Root Directory** to `/backend`.
4. Go to **Variables** tab and add these (copy from your local `.env`):
   - `SUPABASE_URL`: `https://...`
   - `SUPABASE_KEY`: `eyJ...`
   - `SUPABASE_JWT_SECRET`: `...`
   - `FRONTEND_URL`: `https://your-frontend-url.up.railway.app` (You will get this in Step 4)
   - `PORT`: `8000`

5. Go to **Settings** → **Networking**.
6. Click **Generate Domain**. Copy this URL (e.g., `backend-production.up.railway.app`).

---

## Step 4: Configure Frontend Service

1. Go back to the project view.
2. Click **+ New** → **GitHub Repo** → Select `gst-automation-mvp` again.
3. Click on the new service card.
4. Go to **Settings** → **General**.
5. Change **Root Directory** to `/frontend`.
6. Go to **Variables** tab and add:
   - `NEXT_PUBLIC_SUPABASE_URL`: (Same as backend)
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`: (Same as backend)
   - `NEXT_PUBLIC_API_URL`: `https://backend-production.up.railway.app` (The URL from Step 3, **add https://**)

7. Go to **Settings** → **Networking**.
8. Click **Generate Domain**. Copy this URL.

---

## Step 5: Final Connection

1. Go back to the **Backend Service** → **Variables**.
2. Update `FRONTEND_URL` with the URL you just generated for the frontend (e.g., `https://frontend-production.up.railway.app`).
3. Railway will automatically redeploy the backend.

---

## 🎉 Done!

Visit your Frontend URL. You should see the login page.
- Sign up/Login works (Supabase)
- Uploads work (Backend)
- Data is saved to Railway's ephemeral disk (Note: For production, we should move JSON storage to Supabase Storage, but for testing this is fine).

### ⚠️ Important Note on Data Persistence
Railway's disk is **ephemeral**. If the backend restarts, **uploaded files and JSON data will be lost**.
For a real production app, we must switch from local file storage (`/data`) to **Supabase Storage**.

**Recommendation**: For this accountant test, warn her that data might disappear if you redeploy. For the next version, I will implement Supabase Storage for permanent file keeping.
