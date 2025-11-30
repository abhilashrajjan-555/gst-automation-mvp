# Generate E-Invoice - Directive

## Goal
Generate a valid E-Invoice JSON payload and obtain Invoice Reference Number (IRN) and QR code from the Invoice Registration Portal (IRP).

## Inputs
- **Invoice Details**: Full invoice object (Seller, Buyer, Items, Values)
- **Transporter Details**: ID, Name, Mode (if applicable)

## Process

### Step 1: Validation
Validate mandatory fields for E-Invoicing:
- Seller & Buyer GSTIN
- HSN Codes (must be valid)
- Pin Codes (must match state)
- Invoice Number format
- Document Type (INV/CRN/DBN)

### Step 2: Construct JSON Payload
Map internal invoice object to IRP schema (e.g., Version 1.1).

```json
{
  "Version": "1.1",
  "TranDtls": { "TaxSch": "GST", "SupTyp": "B2B" },
  "DocDtls": { "Typ": "INV", "No": "INV001", "Dt": "29/11/2025" },
  "SellerDtls": { "Gstin": "...", "LglNm": "..." },
  "BuyerDtls": { "Gstin": "...", "LglNm": "..." },
  "ItemList": [ ... ],
  "ValDtls": { "AssVal": 1000, "CgstVal": 90, "SgstVal": 90, "TotInvVal": 1180 }
}
```

### Step 3: API Call (Mock/Real)
Send payload to IRP API (via GSP or direct).
- **Authentication**: Get Token using Client ID/Secret.
- **Generate IRN**: POST /eivital/v1.04/auth.

### Step 4: Handle Response
- **Success**: Receive `AckNo`, `AckDt`, `Irn`, `SignedQRCode`, `SignedInvoice`.
- **Error**: Parse error codes (e.g., "2150: Duplicate IRN").

### Step 5: Store & Print
- Save IRN and QR code string to DB.
- Generate PDF invoice with QR code embedded.

## Outputs
- **E-Invoice JSON**: With IRN and QR code.
- **PDF Invoice**: Printable format.

## Edge Cases
- **Duplicate Invoice Number**: Handle error gracefully.
- **Invalid HSN**: Prompt user to correct.
- **API Downtime**: Queue request for retry.

## Success Criteria
- ✅ Valid JSON payload generation
- ✅ Successful IRN generation (mock/real)
- ✅ QR code scannable
