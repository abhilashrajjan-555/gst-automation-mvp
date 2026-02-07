# GST Automation MVP

**Automate GST compliance for Indian SMBs. Save 75% time on monthly filing.**

> Built entirely using AI coding assistants (Claude + ChatGPT) by a non-developer.

---

## The Problem

Manual GST filing takes **4-6 hours/month**. Invoice matching errors lead to GST notices. CAs charge ₹2K-5K/month for basic filing. Late filing = ₹200/day penalty + 18% interest.

## The Solution

Upload invoices → Auto-categorize with OCR → Generate GSTR-3B → File in 30 minutes.

**Time Saved:** 75% (4-6 hrs → 1 hr/month)
**Cost Saved:** ₹14K-50K/year

---

## Features

- **Invoice Upload** — PDF, JPG, PNG, Word, Excel via web interface
- **OCR Extraction** — Automatic data extraction (GSTIN, amounts, dates)
- **HSN Matching** — 97 HSN codes with fuzzy matching (75-100% confidence)
- **GSTR-3B Generation** — Complete monthly return JSON, ready for portal upload
- **Dashboard** — Real-time stats (invoices, amounts, tax)
- **Multi-user Auth** — Supabase authentication with JWT
- **Invoice Reconciliation** — GSTR-2A reconciliation (demo mode)
- **Excel Export** — Download invoice data as Excel

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Frontend | Next.js + TypeScript + Tailwind CSS |
| Backend | Python + FastAPI |
| Auth | Supabase (JWT) |
| OCR | Tesseract |
| Storage | JSON files (MVP), Supabase PostgreSQL (production) |

---

## Quick Start

### Prerequisites

```bash
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils
```

### Setup

```bash
git clone https://github.com/abhilashrajjan-555/gst-automation-mvp.git
cd gst-automation-mvp

# Backend
cd backend
pip3 install -r requirements.txt
cp .env.example .env  # Add your Supabase credentials

# Frontend
cd ../frontend
npm install
```

### Run

```bash
# Terminal 1: Backend
cd backend
python3 -m uvicorn api:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

- **App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs

---

## Environment Variables

### Backend (`backend/.env`)
```
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_JWT_SECRET=your-jwt-secret
USER_GSTIN=your-15-char-gstin  # For state code detection
```

### Frontend (`.env.local`)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## Architecture

```
Browser (Next.js + TypeScript)
    │
    ▼  HTTP + JWT Auth
FastAPI Backend
    │
    ├── OCR (Tesseract) → Extract invoice data
    ├── HSN Matcher (fuzzy) → Classify items
    ├── GSTR-3B Generator → Monthly returns
    └── Supabase → Auth + Database
```

---

## Known Limitations (MVP)

- Line item extraction from OCR is basic (uses total amount as single item)
- GSTR-2A reconciliation is in demo mode
- State code for IGST/CGST split defaults to Kerala if USER_GSTIN not set
- No WhatsApp upload yet
- No e-invoice generation yet

---

## License

MIT

---

Built with Python, Next.js, Tesseract OCR, and AI coding assistants.
Inspired by the pain of 11M+ Indian SMBs struggling with GST compliance.
