# 🚀 Quick Start Guide - GST Automation MVP

Get up and running in 15 minutes!

## Prerequisites

- Python 3.8+ installed
- Tesseract OCR installed (see below)
- macOS/Linux (Windows users: use WSL)

---

## Installation

### 1. Install Tesseract OCR

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install poppler-utils  # For PDF support
```

**Windows:**
Download from: https://github.com/UB-Mannheim/tesseract/wiki

---

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Note:** If you get errors, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Test the System

### Test 1: HSN Matcher

Test if HSN code matching works:

```bash
cd backend
python -m app.hsn_matcher "Laptop Dell Inspiron"
```

**Expected output:**
```
Item: Laptop Dell Inspiron
  → HSN: 8471 | GST Rate: 18% | Confidence: 90%
```

---

### Test 2: OCR (Create a Test Invoice First)

Create a simple test invoice using the sample provided:

**Option A: Use provided sample**
```bash
# Download sample invoice (or create one manually)
# For now, we'll create a text-based test file
```

**Option B: Create your own test invoice**
1. Open Microsoft Word/Google Docs
2. Create a simple invoice with:
   - Vendor GSTIN: 27AABCT1234A1Z5
   - Invoice Number: INV-2024-001
   - Date: 15/12/2024
   - Item: Laptop Dell Inspiron 15
   - Amount: ₹50,000
   - CGST: ₹4,500
   - SGST: ₹4,500
   - Total: ₹59,000
3. Save as PDF in `backend/test_invoices/sample1.pdf`

**Test OCR:**
```bash
python -m app.ocr test_invoices/sample1.pdf
```

---

### Test 3: End-to-End Processing

Process a complete invoice:

```bash
python -m app.processor process test_invoices/sample1.pdf --type purchase
```

**What happens:**
1. OCR extracts invoice data
2. System suggests HSN code
3. You confirm (press 'y')
4. Invoice is saved to `data/invoices/`

---

### Test 4: Generate GSTR-3B

After processing at least one invoice:

```bash
python -m app.processor gstr3b 27AABCT1234A1Z5 12 2024
```

**Arguments:**
- `27AABCT1234A1Z5` = Your GSTIN
- `12` = Month (December)
- `2024` = Year

**Output:**
- Prints GSTR-3B summary
- Saves JSON to `backend/data/gstr3b_12_2024.json`

---

## Directory Structure After Setup

```
gst-automation-mvp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── ocr.py              ✅ OCR extraction
│   │   ├── hsn_matcher.py      ✅ HSN matching
│   │   ├── gstr3b.py           ✅ GSTR-3B generator
│   │   └── processor.py        ✅ Main orchestrator
│   ├── data/
│   │   ├── hsn_master.json     ✅ 100 HSN codes database
│   │   ├── invoices/           📁 Processed invoices (auto-created)
│   │   └── gstr3b_12_2024.json 📄 Generated GSTR-3B
│   ├── test_invoices/
│   │   └── sample1.pdf         📄 Your test invoice
│   ├── requirements.txt        ✅
│   └── uploads/                📁 Temporary uploads (auto-created)
├── directives/
│   └── categorize_invoice.md   ✅ Business logic documentation
└── QUICKSTART.md              ✅ This file
```

---

## Usage Examples

### Process Multiple Invoices

```bash
# Process a purchase invoice
python -m app.processor process invoice1.pdf --type purchase

# Process a sales invoice
python -m app.processor process invoice2.pdf --type sales

# Auto-confirm high-confidence HSN matches (>85%)
python -m app.processor process invoice3.pdf --auto-confirm
```

### Generate GSTR-3B for Any Month

```bash
# November 2024
python -m app.processor gstr3b 27AABCT1234A1Z5 11 2024

# December 2024
python -m app.processor gstr3b 27AABCT1234A1Z5 12 2024 --output my_gstr3b.json
```

### Test HSN Matching for Different Items

```bash
python -m app.hsn_matcher "Software Development"
python -m app.hsn_matcher "Cement"
python -m app.hsn_matcher "Restaurant Services"
```

---

## Common Issues & Solutions

### Issue 1: Tesseract not found
**Error:** `TesseractNotFoundError`

**Solution:**
```bash
# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
```

---

### Issue 2: PDF processing fails
**Error:** `pdf2image` error

**Solution:**
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils
```

---

### Issue 3: Low OCR confidence
**Problem:** OCR confidence < 50%

**Solutions:**
- Ensure invoice is typed (not handwritten)
- Use high-resolution scan (300 DPI+)
- Check if invoice is clear and readable
- Try converting PDF to image first

---

### Issue 4: No HSN match found
**Problem:** Item description too generic

**Solutions:**
- Be more specific (e.g., "Laptop" instead of "Electronics")
- Manually select HSN code when prompted
- System will learn from your selection

---

## What to Test

### Minimum Viable Test Plan (15 mins)

1. **Install dependencies** (5 mins)
   ```bash
   brew install tesseract  # or apt-get
   pip install -r requirements.txt
   ```

2. **Test HSN matcher** (2 mins)
   ```bash
   python -m app.hsn_matcher "Laptop"
   ```

3. **Create test invoice** (5 mins)
   - Use Word/Google Docs
   - Save as PDF in `test_invoices/`

4. **Process invoice** (3 mins)
   ```bash
   python -m app.processor process test_invoices/sample1.pdf --type purchase
   ```

5. **Generate GSTR-3B** (1 min)
   ```bash
   python -m app.processor gstr3b YOUR_GSTIN 12 2024
   ```

---

## Next Steps

### After successful testing:

1. **Process Real Invoices**
   - Use your actual business invoices
   - Build up invoice database

2. **Validate GSTR-3B**
   - Compare generated JSON with manual calculation
   - Verify tax amounts match

3. **Learn from Corrections**
   - System stores your HSN selections
   - Future matches improve automatically

4. **Add More Features** (Week 2-3)
   - Web interface
   - User authentication
   - Database integration

---

## Success Criteria

✅ **You've successfully set up the MVP if:**

1. HSN matcher suggests correct codes (>80% accuracy)
2. OCR extracts GSTIN, invoice number, amounts (>70% confidence)
3. GSTR-3B JSON generates without errors
4. Tax calculations match manual verification

---

## Getting Help

### Check Logs
```bash
# Run with verbose output
python -m app.processor process invoice.pdf --type purchase -v
```

### Validate JSON
```bash
# Check if GSTR-3B JSON is valid
python -c "import json; print(json.load(open('data/gstr3b_12_2024.json')))"
```

### Debug OCR
```bash
# Extract raw text
python -m app.ocr test_invoices/sample1.pdf > output.txt
cat output.txt
```

---

## Performance Benchmarks

**Expected performance on modern laptop:**
- OCR extraction: 5-10 seconds per invoice
- HSN matching: <1 second
- GSTR-3B generation: 1-2 seconds for 50 invoices

---

## Cost Analysis (MVP Phase)

### Free Tier Setup:
- ✅ Tesseract OCR: Free
- ✅ Python: Free
- ✅ Local storage: Free
- ✅ No API costs

**Total MVP cost: ₹0** 🎉

---

## What's Not Included (Yet)

❌ Web interface (coming in Phase 2)
❌ User authentication
❌ Database (using JSON files for MVP)
❌ WhatsApp upload
❌ Payment integration
❌ E-invoice generation

**Focus:** Get core functionality working first!

---

## Ready to Go?

Run this one-liner to test everything:

```bash
cd backend && \
python -m app.hsn_matcher "Laptop" && \
echo "✅ HSN Matcher works!" && \
python -m app.gstr3b && \
echo "✅ All systems ready!"
```

---

**Questions?** Check the main README or raise an issue!

**Working?** Congratulations! You have a functional GST automation tool 🎉
