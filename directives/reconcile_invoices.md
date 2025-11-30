# Reconcile Invoices - Directive

## Goal
Match user's purchase register (books) with supplier's GSTR-2A/2B (portal) to identify discrepancies and maximize ITC claim.

## Inputs
- **Purchase Register**: List of purchase invoices from local DB
- **GSTR-2A/2B**: JSON/Excel downloaded from GST portal

## Process

### Step 1: Data Normalization
Normalize fields for comparison:
- GSTIN: Uppercase, trimmed
- Invoice Number: Remove special chars, lowercase (e.g., "INV-001" -> "inv001")
- Date: Standardize to YYYY-MM-DD
- Amount: Round to 2 decimal places

### Step 2: Exact Matching
Match records where:
`Supplier GSTIN + Invoice Number + Financial Year` match exactly.
AND `Taxable Value` and `Tax Amount` match (within small tolerance, e.g., ₹1).

### Step 3: Fuzzy Matching
For remaining unmatched invoices:
- Match on `Supplier GSTIN` AND `Date` (approx) AND `Amount` (exact).
- Detect likely invoice number typos (e.g., "0" vs "O", "I" vs "1").
- Use Levenshtein distance for invoice numbers.

### Step 4: Categorize Results
- **Matched**: Perfect match. ITC fully eligible.
- **Mismatch**: Invoice found but details differ (e.g., tax amount mismatch).
- **Missing in 2A**: Present in books, not in portal. (Supplier hasn't filed GSTR-1).
- **Missing in Books**: Present in portal, not in books. (Forgot to record purchase?).

## Outputs
- **Reconciliation Report**: JSON/PDF
- **Action Items**:
    - "Contact Supplier X for missing invoice Y"
    - "Correct amount in books for invoice Z"

## Edge Cases
- **Round-off differences**: Allow tolerance of +/- ₹2.
- **Date format mismatch**: Handle DD-MM-YYYY vs MM-DD-YYYY.
- **Amended Invoices**: Handle GSTR-2A amendments (updates to previous invoices).

## Success Criteria
- ✅ Identify 100% of exact matches
- ✅ Flag mismatches with specific reason (e.g., "Tax amount differs by ₹500")
- ✅ Generate clear action list for user
