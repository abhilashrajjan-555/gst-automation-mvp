# Deployment Guide - GST Automation

## 🚀 Quick Deploy with Docker

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Supabase account ([Sign up](https://supabase.com))

### Step 1: Configure Environment Variables

Create a `.env` file in the project root:

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-public-key
```

### Step 2: Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### Step 3: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Step 4: Stop Services

```bash
docker-compose down
```

---

## ☁️ Deploy to Cloud (Railway)

Railway is the easiest way to deploy this app to production.

### Option 1: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Option 2: Deploy via GitHub

1. Push your code to GitHub
2. Go to [Railway](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Add environment variables in Railway dashboard:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

Railway will automatically detect the Dockerfile and deploy.

---

## 🌐 Deploy to Other Platforms

### Render.com

1. Create account at [Render](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - **Build Command**: `docker build -t backend ./backend`
   - **Start Command**: `docker run -p 8000:8000 backend`
5. Add environment variables

### AWS / Google Cloud

Use the provided `Dockerfile` to deploy to:
- AWS ECS (Elastic Container Service)
- Google Cloud Run
- Azure Container Instances

---

## 📊 Production Checklist

Before going live, ensure:

- [ ] Supabase database is set up (run `backend/database/schema.sql`)
- [ ] Environment variables are configured
- [ ] SSL/HTTPS is enabled (Railway/Render do this automatically)
- [ ] Domain name is configured (optional)
- [ ] Backup strategy is in place for Supabase data

---

## 🔧 Troubleshooting

### "Tesseract not found" error
- Ensure Dockerfile includes `tesseract-ocr` installation
- Rebuild: `docker-compose build --no-cache`

### "Poppler not found" error
- Ensure Dockerfile includes `poppler-utils`
- Rebuild: `docker-compose build --no-cache`

### Frontend can't reach backend
- Check `NEXT_PUBLIC_API_URL` environment variable
- Ensure both services are running: `docker-compose ps`

---

## 📞 Support

For deployment issues, check:
1. Docker logs: `docker-compose logs`
2. Backend logs: `docker-compose logs backend`
3. Frontend logs: `docker-compose logs frontend`
