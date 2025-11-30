# GST Automation MVP - Testing Guide

## Current Status: ⚠️ **ALMOST READY** - Components Need to be Created

The UI framework is set up, but we need to create the React components before testing.

---

## Quick Start (3 Steps)

### Step 1: Create React Components

Run this command to create all necessary components:

```bash
cd /Users/abhilashrajan/Developer/antigravity/gst-automation-mvp/frontend

# Create components directory if needed
mkdir -p components

# You'll need to create these 4 files manually or let me create them:
# 1. components/Dashboard.tsx
# 2. components/InvoiceUpload.tsx
# 3. components/InvoiceList.tsx
# 4. components/GSTR3BGenerator.tsx
```

### Step 2: Start the Backend API

Open Terminal 1:
```bash
cd /Users/abhilashrajan/Developer/antigravity/gst-automation-mvp/backend
python3 api.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Start the Frontend

Open Terminal 2:
```bash
cd /Users/abhilashrajan/Developer/antigravity/gst-automation-mvp/frontend
npm run dev
```

Expected output:
```
 ▲ Next.js 15.x.x
  - Local:        http://localhost:3000
  - Environments: .env.local

 ✓ Starting...
 ✓ Ready in 2.3s
```

---

## What's Been Completed

✅ **Backend:**
- FastAPI server with REST endpoints (`backend/api.py`)
- Invoice processing (`backend/app/processor.py`)
- HSN matcher (`backend/app/hsn_matcher.py`)
- GSTR-3B generator (`backend/app/gstr3b.py`)
- All dependencies installed
- Tesseract OCR configured

✅ **Frontend Framework:**
- Next.js 15 initialized
- TypeScript + Tailwind CSS configured
- Main page layout (`app/page.tsx`)
- Tab navigation (Dashboard, Upload, Invoices, GSTR-3B)

⚠️ **Pending:**
- 4 React components need to be created
- Then ready to test!

---

## Components to Create

I'll create these for you. Here's what each component does:

### 1. Dashboard.tsx
- Shows stats (total invoices, amounts, tax)
- Visual cards with icons
- Processing accuracy meter
- Fetches from `/api/stats`

### 2. InvoiceUpload.tsx
- File upload drag-and-drop interface
- Select invoice type (Sales/Purchase)
- Upload progress indicator
- Success/error messages
- Posts to `/api/upload-invoice`

### 3. InvoiceList.tsx
- Table of all processed invoices
- Columns: Date, Invoice#, Amount, Type, Status
- Click to view details
- Fetches from `/api/invoices`

### 4. GSTR3BGenerator.tsx
- Form with GSTIN, Month, Year
- Generate button
- Display generated return data
- Download JSON option
- Posts to `/api/generate-gstr3b`

---

## Testing Workflow (Once Components are Ready)

### Test 1: Dashboard
1. Open http://localhost:3000
2. Should show "Welcome to GST Automation"
3. Stats cards should display (will show 0 initially)
4. No errors in browser console

### Test 2: Upload Invoice
1. Click "Upload Invoice" tab
2. Drag/drop a test PDF or select file
3. Choose "Purchase" or "Sales"
4. Click Upload
5. Should show "Processing..." then "Success!"
6. Invoice appears in backend/data/invoices/

### Test 3: View Invoices
1. Click "Invoice List" tab
2. Should show uploaded invoices in table
3. Click row to see details
4. Verify amounts, GST calculations

### Test 4: Generate GSTR-3B
1. Click "GSTR-3B" tab
2. Enter GSTIN (e.g., 29AABCT1234A1Z5)
3. Select month/year (e.g., December 2024)
4. Click "Generate"
5. Should display return summary
6. JSON file created in backend/data/

---

## API Endpoints Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/api/health` | GET | Detailed status |
| `/api/stats` | GET | Dashboard statistics |
| `/api/invoices` | GET | List all invoices |
| `/api/upload-invoice` | POST | Upload & process invoice |
| `/api/generate-gstr3b` | POST | Generate return |
| `/api/suggest-hsn` | POST | Get HSN suggestions |

---

## Troubleshooting

### Backend Not Starting
```bash
# Check if port 8000 is in use
lsof -i :8000

# If blocked, kill process
kill -9 <PID>

# Restart
python3 backend/api.py
```

### Frontend Not Starting
```bash
# Check if port 3000 is in use
lsof -i :3000

# If blocked, use different port
PORT=3001 npm run dev
```

### CORS Errors
- Backend already configured for localhost:3000 and :3001
- Check browser console for specific errors

### File Upload Fails
- Check backend/uploads/ directory exists
- Verify file is PDF/JPG/PNG
- Check file size (< 10MB recommended)

---

## Next Steps

**Let me create the 4 components for you, then:**

1. Start backend: `python3 backend/api.py`
2. Start frontend: `npm run dev`
3. Open http://localhost:3000
4. Test all features!

Would you like me to create the components now?
