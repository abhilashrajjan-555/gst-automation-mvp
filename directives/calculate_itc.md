# Calculate ITC - Directive

## Goal
Calculate the eligible Input Tax Credit (ITC) for a given period, applying blocking rules and reversals.

## Inputs
- **Purchase Invoices**: Categorized invoices
- **GSTR-2B Status**: Whether invoice appears in GSTR-2B (auto-drafted ITC statement)

## Process

### Step 1: Eligibility Check (Section 16)
For each invoice, check:
- Possession of tax invoice? (Yes)
- Goods/Services received? (Yes)
- Supplier has paid tax? (Assumed Yes if in 2B)
- Return filed? (Yes)

### Step 2: Blocked Credits (Section 17(5))
Flag invoices ineligible for ITC based on HSN/Category:
- Motor vehicles (unless for transport business)
- Food and beverages, outdoor catering
- Membership of clubs, health centers
- Construction of immovable property (for own use)

*Logic*: Maintain a list of "Blocked HSNs" or keywords.

### Step 3: Reversals
Calculate reversals for:
- Goods returned
- Exempt supplies (Rule 42/43) - Pro-rata reversal
- Payment not made to supplier within 180 days

### Step 4: Final Calculation
`Net ITC = (Total ITC in 2B) - (Ineligible ITC) - (Reversals)`

## Outputs
- **ITC Summary**:
    - Eligible ITC (IGST, CGST, SGST)
    - Ineligible ITC (with reasons)
    - Reversals required

## Edge Cases
- **Partial Business Use**: If goods used partly for personal use, reverse proportionate ITC.
- **180 Day Rule**: Track invoice dates and flag if unpaid > 180 days.

## Success Criteria
- ✅ Correctly flag common blocked credits (e.g., food expenses)
- ✅ Match GSTR-2B figures
