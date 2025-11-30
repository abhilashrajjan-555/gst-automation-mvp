# Sample Invoice Template

Use this template to create test invoices in Word/Google Docs, then save as PDF.

---

## Sample Invoice #1 - Purchase Invoice

```
                        TAX INVOICE

Tech Supplies Pvt Ltd
123 MG Road, Bangalore, Karnataka - 560001
GSTIN: 29AABCT1234A1Z5
Phone: +91-80-12345678

Invoice No: INV-2024-001
Date: 15/12/2024

Bill To:
ABC Enterprises
456 Park Street, Bangalore - 560002
GSTIN: 29AABCE5678B1Z3

┌────────────────────────────────────────────────────────────┐
│ Item Description          │ Qty │  Rate   │   Amount       │
├────────────────────────────────────────────────────────────┤
│ Laptop Dell Inspiron 15   │  1  │ 50,000  │   50,000.00    │
│ (Model: Inspiron 3511)    │     │         │                │
│ HSN: 8471                 │     │         │                │
└────────────────────────────────────────────────────────────┘

                                    Taxable Value:   ₹50,000.00
                                    CGST @ 9%:       ₹ 4,500.00
                                    SGST @ 9%:       ₹ 4,500.00
                                    ─────────────────────────────
                                    Total Amount:    ₹59,000.00
                                    ═════════════════════════════

Amount in Words: Fifty-Nine Thousand Rupees Only

Bank Details:
Bank: HDFC Bank
Account: 1234567890
IFSC: HDFC0001234

For Tech Supplies Pvt Ltd


_________________
Authorized Signatory
```

---

## Sample Invoice #2 - Service Invoice

```
                        TAX INVOICE

Digital Solutions India
789 Tech Park, Pune, Maharashtra - 411001
GSTIN: 27AABCD9876C1Z8
Email: billing@digitalsolutions.in

Invoice No: SRV/2024/042
Date: 20/12/2024

Bill To:
XYZ Retail Ltd
101 Commercial Complex, Pune - 411002
GSTIN: 27AABCX1234D1Z9

┌────────────────────────────────────────────────────────────┐
│ Description                │ Qty │  Rate   │   Amount      │
├────────────────────────────────────────────────────────────┤
│ Website Development       │  1  │100,000  │  100,000.00   │
│ (Custom E-commerce Site)  │     │         │               │
│ SAC: 998314               │     │         │               │
│                           │     │         │               │
│ Monthly Hosting & Support │  1  │  5,000  │    5,000.00   │
│ SAC: 998314               │     │         │               │
└────────────────────────────────────────────────────────────┘

                                    Taxable Value:  ₹105,000.00
                                    CGST @ 9%:      ₹  9,450.00
                                    SGST @ 9%:      ₹  9,450.00
                                    ─────────────────────────────
                                    Total Amount:   ₹123,900.00
                                    ═════════════════════════════

Amount in Words: One Lakh Twenty-Three Thousand Nine Hundred Rupees Only

Payment Terms: Net 30 days
Due Date: 19/01/2025

_________________
Authorized Signatory
```

---

## Sample Invoice #3 - Retail Invoice

```
                        RETAIL INVOICE

Fashion Point
56 Brigade Road, Bangalore, Karnataka - 560001
GSTIN: 29AABCF5432G1Z1
Phone: +91-80-98765432

Invoice No: RTL-2024-1523
Date: 18/12/2024

Customer: Walk-in Customer

┌────────────────────────────────────────────────────────────┐
│ Item                      │ Qty │  Rate   │   Amount       │
├────────────────────────────────────────────────────────────┤
│ Men's Cotton T-Shirt      │  3  │   399   │    1,197.00    │
│ HSN: 6109                 │     │         │                │
│                           │     │         │                │
│ Denim Jeans               │  2  │ 1,499   │    2,998.00    │
│ HSN: 6203                 │     │         │                │
│                           │     │         │                │
│ Sports Shoes              │  1  │ 2,999   │    2,999.00    │
│ HSN: 6404                 │     │         │                │
└────────────────────────────────────────────────────────────┘

                                    Taxable Value:   ₹7,194.00
                                    CGST @ 2.5%:     ₹  179.85
                                    SGST @ 2.5%:     ₹  179.85
                                    ─────────────────────────────
                                    Total Amount:    ₹7,553.70
                                    ═════════════════════════════

Amount in Words: Seven Thousand Five Hundred Fifty-Three Rupees and Seventy Paise Only

Payment Mode: Cash

Thank you for shopping with us!
```

---

## How to Use These Templates

### Method 1: Microsoft Word/Google Docs

1. Copy the text above
2. Paste into Word/Google Docs
3. Format nicely (use monospace font like Courier for tables)
4. Save as PDF: `File > Save As > PDF`
5. Place in `backend/test_invoices/` folder

### Method 2: Online Invoice Generator

1. Use free tools like:
   - https://invoice-generator.com
   - https://www.zoho.com/invoice/free-invoice-generator.html
2. Fill in details from template above
3. Download PDF
4. Rename to `sample1.pdf`, `sample2.pdf`, etc.

### Method 3: Use Real Invoices

1. Take your actual business invoices
2. Ensure they have:
   - GSTIN (15 characters)
   - Invoice number
   - Date
   - Item descriptions
   - GST amounts (CGST/SGST/IGST)
   - Total amount
3. Save as PDF in `test_invoices/` folder

---

## Testing Checklist

After creating invoices, test:

- ✅ OCR extracts GSTIN correctly
- ✅ Invoice number is detected
- ✅ Date is parsed (DD/MM/YYYY format works best)
- ✅ Total amount matches
- ✅ GST amounts (CGST/SGST) are extracted
- ✅ HSN codes are suggested for items

---

## Common Formats That Work Well

### Good Invoice Formats:
✅ Typed text (not handwritten)
✅ Clear fonts (Arial, Times New Roman)
✅ High contrast (black text on white)
✅ 300 DPI or higher scans
✅ PDF or JPG format

### Formats That May Fail:
❌ Handwritten invoices
❌ Low-resolution scans (<150 DPI)
❌ Faded or blurry text
❌ Colored backgrounds
❌ Complex table layouts

---

## Next Steps

1. Create 2-3 test invoices using templates above
2. Save as PDF in `backend/test_invoices/`
3. Run: `python -m app.processor process test_invoices/sample1.pdf --type purchase`
4. Verify extracted data
5. Generate GSTR-3B

---

**Tip:** Start with simple, single-item invoices to test the system, then move to complex multi-item invoices.
