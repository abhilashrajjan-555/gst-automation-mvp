# GST Automation MVP

Full-stack GST workflow automation prototype for Indian SMB operations.
Upload invoices, extract structured data with OCR, and generate GSTR-3B outputs.

## Overview

This project demonstrates an end-to-end GST processing flow with a Next.js frontend and FastAPI backend.

- Upload single or bulk invoices from the web app
- Extract invoice fields using OCR
- Categorize data and generate GSTR-3B JSON outputs
- Review dashboard metrics and export processed data
- Support authenticated usage with Supabase

## Problem

GST workflows for small businesses can involve repeated manual invoice review, field extraction, tax categorization, and return preparation. That is slow, error-prone, and hard to scale without a structured process.

## Solution

This MVP turns invoice files into a reviewable GST workflow: upload invoices, extract core fields with OCR, classify the data, and generate GSTR-3B-style outputs for review.

## Key Features

- Invoice upload (`/api/upload-invoice`, `/api/upload-bulk`)
- OCR-driven extraction for GSTIN, invoice metadata, and totals
- HSN matching and tax classification support
- GSTR-3B generation endpoint (`/api/generate-gstr3b`)
- Invoice listing, updates, and Excel export
- GSTR-2A reconciliation endpoint in demo mode

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | Next.js 16, TypeScript, Tailwind CSS |
| Backend | Python, FastAPI, Uvicorn |
| OCR | Tesseract + pytesseract + pdf2image |
| Auth/Data | Supabase (Auth + DB integration) |
| Data Files | JSON and Excel exports for MVP workflows |

## Repository Structure

```text
gst-automation-mvp/
├── frontend/            # Next.js UI
├── backend/             # FastAPI API + processing pipeline
├── backend/app/         # OCR, processor, HSN matcher, auth, DB helpers
├── backend/data/        # Generated reports and exports
├── backend/test_system.py
└── docker-compose.yml
```

## Local Setup

### 1. System dependencies

```bash
# macOS
brew install tesseract poppler

# Ubuntu / Debian
sudo apt-get install tesseract-ocr poppler-utils
```

### 2. Clone and install

```bash
git clone https://github.com/abhilashrajjan-555/gst-automation-mvp.git
cd gst-automation-mvp

# Backend
cd backend
pip3 install -r requirements.txt
cp .env.example .env

# Frontend
cd ../frontend
npm install
```

### 3. Configure environment

Backend (`backend/.env`):

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
SUPABASE_JWT_SECRET=your-jwt-secret
USER_GSTIN=your-15-char-gstin
```

Frontend (`frontend/.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

### 4. Run services

```bash
# Terminal 1
cd backend
python3 -m uvicorn api:app --reload --port 8000

# Terminal 2
cd frontend
npm run dev
```

- App: [http://localhost:3000](http://localhost:3000)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Docker (Optional)

```bash
docker compose up --build
```

## API Surface (Selected)

- `GET /api/health`
- `POST /api/upload-invoice`
- `POST /api/upload-bulk`
- `GET /api/invoices`
- `POST /api/generate-gstr3b`
- `POST /api/reconcile-gstr2a` (demo behavior)

## Current MVP Limitations

- OCR line-item extraction is simplified for some invoice formats
- Reconciliation endpoint currently runs in demo mode
- Data persistence is optimized for MVP workflows, not full production scale

## What This Shows

- Full-stack workflow automation design
- FastAPI backend with a Next.js frontend
- OCR processing pipeline for document-heavy operations
- Authenticated MVP structure using Supabase
- Clear separation between prototype capability and production limitations

## License

MIT.
