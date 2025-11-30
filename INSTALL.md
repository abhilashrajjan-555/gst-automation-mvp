# Installation & Setup Guide

## Prerequisites

### 1. Install System Dependencies

#### macOS
```bash
# Install Tesseract OCR
brew install tesseract

# Install Poppler (for PDF processing)
brew install poppler
```

#### Ubuntu/Debian
```bash
# Install Tesseract OCR
sudo apt-get update
sudo apt-get install tesseract-ocr

# Install Poppler
sudo apt-get install poppler-utils
```

#### Windows
```powershell
# Install Tesseract OCR
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH

# Install Poppler
# Download from: https://github.com/oschwartz10612/poppler-windows/releases
# Add to PATH
```

### 2. Verify Installation
```bash
# Check Tesseract
tesseract --version
# Expected: tesseract 5.x.x

# Check Poppler
pdftoppm -v
# Expected: pdftoppm version 24.x.x
```

## Project Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd gst-automation-mvp
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip3 install -r requirements.txt

# Verify installation
python3 -c "import pytesseract, pdf2image; print('✅ All dependencies installed')"
```

### 3. Frontend Setup
```bash
cd frontend

# Install Node dependencies
npm install

# Verify installation
npm list next react
```

## Running the Application

### Option 1: Manual Start (Development)

**Terminal 1 - Backend:**
```bash
cd backend
python3 -m uvicorn api:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Option 2: Production Build

**Backend:**
```bash
cd backend
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

## Access Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/health

## Troubleshooting

### Issue: "Poppler not installed" error

**Solution:**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

### Issue: "Tesseract not found" error

**Solution:**
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Verify
tesseract --version
```

### Issue: PDF processing fails

**Symptoms:** 500 error when uploading PDF files

**Solution:**
1. Ensure Poppler is installed: `pdftoppm -v`
2. Restart the backend server
3. Check backend logs for detailed error

### Issue: Low OCR accuracy

**Symptoms:** Confidence < 50%, missing data

**Solutions:**
1. Use high-quality scans (300 DPI or higher)
2. Ensure invoice is typed (not handwritten)
3. Check if invoice is in English
4. For Hindi/regional languages: `brew install tesseract-lang`

### Issue: Port already in use

**Symptoms:** "Address already in use" error

**Solution:**
```bash
# Kill process on port 8000
lsof -i :8000 -t | xargs kill -9

# Kill process on port 3000
lsof -i :3000 -t | xargs kill -9
```

## Testing

### Test OCR Extraction
```bash
cd backend
python3 -m app.ocr test_invoices/sample_invoice_generated.png
```

### Test HSN Matching
```bash
cd backend
python3 -m app.hsn_matcher "Laptop Dell Inspiron"
```

### Test Full System
```bash
cd backend
python3 test_system.py
```

### Test with Real Invoice
```bash
cd backend
python3 -m app.processor process /path/to/invoice.pdf --type purchase --auto-confirm
```

## Performance Optimization (Optional)

### Install Faster Fuzzy Matching
```bash
pip3 install python-Levenshtein
```
This speeds up HSN matching by 3-5x.

### Install Additional Tesseract Languages
```bash
# For Hindi invoices
brew install tesseract-lang

# Verify
tesseract --list-langs
```

## Next Steps

1. **Upload a test invoice** via http://localhost:3000
2. **Check the dashboard** for statistics
3. **Generate GSTR-3B** for a test month
4. **Review the documentation** in `/docs`

## Support

If you encounter issues:
1. Check this guide first
2. Review backend logs in the terminal
3. Check `/docs/TESTING_GUIDE.md`
4. Verify all dependencies are installed
