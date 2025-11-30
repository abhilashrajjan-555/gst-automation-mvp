# Onboarding - Directive

## Goal
Onboard a new user by collecting their business details, validating their GSTIN, and setting up their profile for automation.

## Inputs
- **GSTIN**: 15-character Goods and Services Tax Identification Number
- **Business Name**: Legal name of the business
- **Turnover**: Annual turnover (optional, for tier suggestion)
- **Contact Details**: Email, Phone

## Process

### Step 1: GSTIN Validation
Validate the format of the provided GSTIN.
Format: `\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}`

```python
import re

def validate_gstin(gstin):
    pattern = r'\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}'
    return bool(re.match(pattern, gstin))
```

### Step 2: Fetch Business Details (Mock/API)
Fetch business details from GST portal API (or mock for MVP).
- Legal Name
- Trade Name
- Registration Date
- Taxpayer Type (Regular/Composition)
- State/Center Jurisdiction

### Step 3: Profile Creation
Create a user profile JSON.

```json
{
  "gstin": "27AABCT1234A1Z5",
  "legal_name": "Tech Solutions",
  "trade_name": "Tech Solutions",
  "registration_date": "2022-04-01",
  "taxpayer_type": "Regular",
  "turnover_bracket": "1.5Cr - 5Cr",
  "contact": {
    "email": "admin@techsolutions.com",
    "phone": "9876543210"
  },
  "preferences": {
    "default_hsn_category": "Services",
    "notification_language": "English"
  },
  "created_at": "2025-11-29T10:00:00"
}
```

### Step 4: Tier Suggestion
Based on turnover and business type, suggest a subscription tier.
- < 20L: Free/Basic
- 20L - 1.5Cr: Pro
- > 1.5Cr: Premium

## Outputs
- **User Profile JSON**: Saved to `backend/data/users/{gstin}.json`
- **Onboarding Status**: Complete/Pending

## Edge Cases
- **Invalid GSTIN**: Prompt user to re-enter.
- **Cancelled GSTIN**: Flag as inactive, warn user.
- **API Failure**: Allow manual entry of details if API fails.

## Success Criteria
- ✅ Valid GSTIN format
- ✅ User profile created successfully
- ✅ Tier suggested correctly
