# Generate GSTR-3B - Directive

## Goal
Generate the monthly GSTR-3B return summary based on categorized sales and purchase invoices.

## Inputs
- **GSTIN**: User's GSTIN
- **Month/Year**: Return period (e.g., 12/2024)
- **Categorized Invoices**: List of invoices for the period

## Process

### Step 1: Aggregate Outward Supplies (Sales)
Sum up all sales invoices to populate Table 3.1.
- **3.1(a)**: Outward taxable supplies (other than zero rated, nil rated and exempted)
- **3.1(b)**: Outward taxable supplies (zero rated)
- **3.1(c)**: Other outward supplies (Nil rated, exempted)

```python
def calculate_outward_supplies(sales_invoices):
    taxable_value = sum(inv['taxable_amount'] for inv in sales_invoices)
    igst = sum(inv['igst'] for inv in sales_invoices)
    cgst = sum(inv['cgst'] for inv in sales_invoices)
    sgst = sum(inv['sgst'] for inv in sales_invoices)
    return {
        "taxable_value": taxable_value,
        "igst": igst,
        "cgst": cgst,
        "sgst": sgst
    }
```

### Step 2: Calculate Eligible ITC (Purchases)
Sum up all eligible purchase invoices to populate Table 4.
- **4(A)**: ITC Available (Import of goods, services, Inward supplies liable to reverse charge, All other ITC)
- **4(B)**: ITC Reversed
- **4(C)**: Net ITC Available (A - B)

```python
def calculate_itc(purchase_invoices):
    eligible_invoices = [inv for inv in purchase_invoices if inv['itc_eligible']]
    # Sum up IGST, CGST, SGST
    # ...
```

### Step 3: Calculate Net Tax Liability
Table 6.1: Payment of Tax
- Tax Payable = Output Tax (from Step 1)
- Paid through ITC = Min(Tax Payable, Available ITC)
- Paid in Cash = Tax Payable - Paid through ITC

### Step 4: Generate JSON
Construct the final JSON structure required by GST portal.

```json
{
  "gstin": "27AABCT1234A1Z5",
  "ret_period": "122024",
  "sup_details": {
    "osup_det": {
      "txval": 100000,
      "iamt": 18000,
      "camt": 0,
      "samt": 0
    }
  },
  "itc_elg": {
    "itc_avl": [
      {
        "ty": "ALL",
        "iamt": 5000,
        "camt": 2500,
        "samt": 2500
      }
    ]
  }
}
```

## Outputs
- **GSTR-3B JSON**: Saved to `backend/data/returns/gstr3b_{gstin}_{period}.json`
- **Summary Report**: Text/PDF summary for user review

## Edge Cases
- **Negative Liability**: Should not happen in 3B (carry forward).
- **Late Fees**: Calculate if filing after due date (20th of next month).
- **Interest**: Calculate @ 18% p.a. for delayed payment.

## Success Criteria
- ✅ JSON structure matches GST portal schema
- ✅ Calculations match manual verification
- ✅ ITC correctly separated into IGST/CGST/SGST heads
