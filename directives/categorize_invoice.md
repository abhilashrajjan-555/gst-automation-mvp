# Categorize Invoice - Directive

## Goal
Extract invoice details from uploaded files and auto-categorize items by GST rate using HSN code matching.

## Inputs
- **Invoice file**: PDF, JPG, or PNG format
- **User's business type** (optional): For better HSN suggestions
- **User's GSTIN** (optional): For validating supplier GSTINs

## Process

### Step 1: OCR Extraction
Run OCR on the invoice to extract raw text. Use `backend/app/ocr.py`:

```python
from app.ocr import extract_invoice_data

result = extract_invoice_data("path/to/invoice.pdf")
```

**Expected Output**:
```json
{
  "vendor_name": "Tech Supplies Pvt Ltd",
  "vendor_gstin": "27AABCT1234A1Z5",
  "invoice_number": "INV-2024-001",
  "invoice_date": "2024-12-15",
  "line_items": [
    {
      "description": "Laptop Dell Inspiron 15",
      "quantity": 1,
      "rate": 50000,
      "amount": 50000
    }
  ],
  "total_amount": 59000,
  "cgst": 4500,
  "sgst": 4500,
  "igst": 0
}
```

### Step 2: HSN Code Matching
For each line item, match description to HSN code using fuzzy matching:

```python
from app.hsn_matcher import suggest_hsn

for item in result['line_items']:
    hsn_data = suggest_hsn(item['description'])
    item['hsn_code'] = hsn_data['hsn_code']
    item['gst_rate'] = hsn_data['gst_rate']
    item['confidence'] = hsn_data['confidence']
```

**Confidence Levels**:
- **>90%**: Auto-accept
- **70-90%**: Present to user for confirmation
- **<70%**: Ask user to manually select HSN code

### Step 3: User Confirmation
If confidence < 90%, present options to user:

```
Found item: "Laptop Dell Inspiron 15"
Suggested HSN: 8471 (Automatic data processing machines) - 18% GST
Confidence: 85%

Options:
1. Accept (8471 - 18%)
2. Choose different HSN code
3. Enter manually
```

### Step 4: Save Categorized Invoice
Store the categorized invoice with all metadata:

```json
{
  "invoice_id": "unique-id",
  "vendor_gstin": "27AABCT1234A1Z5",
  "invoice_number": "INV-2024-001",
  "invoice_date": "2024-12-15",
  "line_items": [
    {
      "description": "Laptop Dell Inspiron 15",
      "quantity": 1,
      "rate": 50000,
      "amount": 50000,
      "hsn_code": "8471",
      "gst_rate": 18,
      "cgst": 4500,
      "sgst": 4500
    }
  ],
  "total_amount": 59000,
  "categorization_status": "confirmed",
  "processed_at": "2024-12-28T10:30:00"
}
```

## Outputs
- **Categorized invoice JSON**: Saved to `backend/data/invoices/{invoice_id}.json`
- **Confirmation required**: Boolean flag if manual review needed
- **Errors/Warnings**: List of issues (missing GSTIN, ambiguous items, etc.)

## Edge Cases

### 1. Missing GSTIN
If vendor GSTIN is not found:
- Flag as **unregistered supplier**
- Mark ITC (Input Tax Credit) as **not eligible**
- Warn user: "No ITC available for this purchase"

### 2. Ambiguous Items
If item description is too generic (e.g., "Accessories"):
- Present top 3 HSN matches
- Ask user to specify product type
- Learn from user's choice for future

### 3. Handwritten Invoices
If OCR confidence is very low (<50%):
- Reject with message: "Please upload a typed/printed invoice"
- Suggest alternatives: "You can manually enter invoice details"

### 4. Multi-page Invoices
If invoice has multiple pages:
- Process all pages
- Merge line items
- Validate totals match across pages

### 5. Foreign Currency
If amounts are in USD/EUR:
- Use RBI reference rate for the invoice date
- Convert to INR
- Note conversion rate in metadata

### 6. Composite/Exempt Items
If item is GST-exempt (rate = 0%) or composite scheme:
- Mark accordingly
- Don't calculate ITC
- Show in separate section of GSTR-3B

## Validation Rules

### GSTIN Format
Must be exactly 15 characters: `\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}`

Example: `27AABCT1234A1Z5`

### Invoice Number
- Must be unique
- Can contain alphanumeric + special chars (-, /)
- Example: `INV-2024-001`, `TAX/24/0001`

### HSN Code
- Must be 4, 6, or 8 digits
- Validate against official HSN master list
- Example: `8471` (computers), `640399` (footwear)

### GST Rates
Valid rates only: 0%, 3%, 5%, 12%, 18%, 28%

## Success Criteria
- ✅ OCR accuracy >80% for typed invoices
- ✅ HSN matching confidence >85% for common items
- ✅ Processing time <30 seconds per invoice
- ✅ User confirmation required for <20% of items

## Self-Annealing (Continuous Improvement)

### Learning from User Corrections
When user corrects an HSN code:
1. Store correction: `{description: "Laptop Dell", user_selected_hsn: "8471"}`
2. Next time similar item appears, use user's choice
3. Build custom HSN dictionary per user

### Feedback Loop
Track these metrics:
- **Auto-acceptance rate**: % of items not requiring user input
- **OCR accuracy**: Compare extracted totals vs actual
- **Processing errors**: Log failed invoices for manual review

### Improvement Triggers
If auto-acceptance rate <70%:
- Review HSN matching algorithm
- Add more synonyms to HSN database
- Improve OCR preprocessing (image enhancement)

## Integration Points

### Next Step: GSTR-3B Generation
Once invoice is categorized, it feeds into:
- `directives/generate_gstr3b.md`
- Uses categorized invoices to calculate monthly tax liability

### Data Flow
```
Invoice Upload → OCR Extraction → HSN Matching →
User Confirmation → Save to DB → GSTR-3B Calculation
```

## Notes for Developer (Claude)
- Always validate GSTIN format before processing
- Use fuzzy matching (fuzzywuzzy library) for HSN codes
- Store original invoice image for audit trail
- Log all user corrections for continuous learning
- Prioritize accuracy over speed (it's tax compliance!)
- When in doubt, ask user to confirm (better safe than sorry)
