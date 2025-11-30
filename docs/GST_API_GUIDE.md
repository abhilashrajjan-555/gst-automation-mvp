# GST Portal API Integration Guide

## 🏛️ Official GST APIs in India

### 1. **GST Portal APIs** (Government of India)
**Base URL**: `https://api.gst.gov.in/`

**Available APIs**:
- **GSTR-1 API**: Submit sales data
- **GSTR-2A API**: Fetch purchase data uploaded by vendors
- **GSTR-2B API**: Auto-drafted ITC statement
- **GSTR-3B API**: Submit monthly return
- **E-Invoice (IRN) API**: Generate e-invoices via IRP (Invoice Registration Portal)

**Access Requirements**:
1. **GST Registration**: Must have a valid GSTIN
2. **API Credentials**: Apply through GST Portal
3. **Digital Signature**: Class 2/3 DSC required for some operations
4. **IP Whitelisting**: Your server IP must be registered

**Application Process**:
1. Login to GST Portal (https://www.gst.gov.in)
2. Go to Services → User Services → Manage API Access
3. Submit application with:
   - Business details
   - Purpose of API usage
   - Server IP addresses
4. Wait for approval (7-15 days)

---

## 2. **Sandbox Environment** (For Testing)

**Sandbox URL**: `https://sandboxapi.gst.gov.in/`

**How to Get Access**:
1. Register at GST Sandbox Portal
2. Get test GSTIN and credentials
3. Test your integration before going live

**Note**: Sandbox has limited functionality and doesn't reflect real data.

---

## 3. **Third-Party GST APIs** (Easier to Start With)

Since direct GST API access is complex, most startups use third-party aggregators:

### Option A: **ClearTax API**
- **Website**: https://cleartax.in/s/gst-api
- **Features**: GSTR-1, GSTR-2A, GSTR-3B, E-Invoice
- **Pricing**: Pay-per-use (₹1-5 per API call)
- **Setup Time**: 1-2 days
- **Pros**: Easy integration, good documentation
- **Cons**: Ongoing costs

### Option B: **Tally Solutions API**
- **Website**: https://tallysolutions.com
- **Features**: Full GST suite
- **Pricing**: Part of Tally subscription
- **Pros**: Widely used by accountants
- **Cons**: Requires Tally license

### Option C: **MasterIndia GST API**
- **Website**: https://www.masterindia.co
- **Features**: GSTR-2A, GSTR-2B, E-Invoice
- **Pricing**: Subscription-based
- **Pros**: Reliable, used by many ERPs
- **Cons**: Monthly fees

---

## 4. **E-Invoice API (NIC IRP)**

For e-invoice generation, you must use one of the **Invoice Registration Portals (IRPs)**:

### Official IRPs:
1. **NIC IRP**: https://einvoice1.gst.gov.in
2. **CDSL IRP**: https://einvoice2.gst.gov.in
3. **Vayana IRP**: https://einvoice3.gst.gov.in

**API Flow**:
```
Your App → IRP API → GST Portal
```

**Authentication**: 
- Username/Password (from GST Portal)
- API Key (generated in IRP)

---

## 📋 What We Need for Our App

### Phase 1: MVP (Current)
✅ **Manual GSTR-2A Upload**: User downloads from portal, uploads to our app
- **Pros**: No API needed, works immediately
- **Cons**: Manual step for user

### Phase 2: Semi-Automated (Next 3 months)
🔄 **Third-Party API Integration** (ClearTax or MasterIndia)
- **Cost**: ~₹5,000-10,000/month for 100 users
- **Implementation**: 2-3 weeks
- **Features**: Auto-fetch GSTR-2A, submit GSTR-3B

### Phase 3: Fully Automated (6-12 months)
🎯 **Direct GST Portal API**
- **Cost**: Free (but requires compliance)
- **Implementation**: 2-3 months (including approval)
- **Features**: Full control, no middleman

---

## 🚀 Recommended Path for Your App

### Step 1: Launch with Manual Upload (Now)
- Users download GSTR-2A from portal
- Upload Excel/JSON to your app
- Your app does reconciliation
- **Time to Market**: Immediate

### Step 2: Integrate ClearTax API (After 50 users)
- Apply for ClearTax API access
- Implement auto-fetch for GSTR-2A
- **Cost**: ₹5-10/user/month
- **Time**: 2 weeks

### Step 3: Apply for Direct API (After 500 users)
- Submit application to GST Portal
- Get IP whitelisting
- Migrate from ClearTax to direct API
- **Savings**: ₹50,000+/month at scale

---

## 📝 Sample GSTR-2A API Call (ClearTax)

```python
import requests

# ClearTax API endpoint
url = "https://api.cleartax.in/v2/gst/gstr2a/get"

headers = {
    "X-Cleartax-Auth-Token": "your_api_token",
    "Content-Type": "application/json"
}

payload = {
    "gstin": "29AABCT1234A1Z5",
    "return_period": "112025"  # November 2025
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

# data will contain all invoices uploaded by vendors
for invoice in data['invoices']:
    print(f"Vendor: {invoice['ctin']}")
    print(f"Invoice #: {invoice['inum']}")
    print(f"Amount: {invoice['val']}")
```

---

## ⚠️ Important Legal Notes

1. **Data Privacy**: GST data is sensitive. Ensure encryption and compliance with IT Act.
2. **Accuracy**: Any errors in submitted data can lead to penalties.
3. **Audit Trail**: Maintain logs of all API calls for 6 years (GST requirement).
4. **Rate Limiting**: GST APIs have strict rate limits (10-20 calls/minute).

---

## 🎯 For Your Accountant Testing

**What to tell her**:
1. "We currently support manual GSTR-2A upload (download from portal, upload here)"
2. "We're applying for ClearTax API to automate this in 2 months"
3. "The reconciliation logic is already built and ready"

This shows you understand the real workflow and have a roadmap.

---

## 📞 Next Steps

1. **Immediate**: Implement manual GSTR-2A upload (I'll do this now)
2. **Week 1**: Test with your accountant
3. **Week 2**: Apply for ClearTax API (if she approves)
4. **Month 3**: Integrate ClearTax API
5. **Month 6**: Apply for direct GST API access

**Cost Projection**:
- 0-50 users: ₹0 (manual upload)
- 50-500 users: ₹10,000/month (ClearTax)
- 500+ users: ₹0 (direct API, but requires compliance team)
