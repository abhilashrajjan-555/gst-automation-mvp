# 🧪 How to Test Multi-User Isolation

Now that we have Authentication and Data Isolation, here is how you verify it works.

## Prerequisite
Ensure both Frontend and Backend servers are running.

## Step 1: Create Two Different Users

1. Open **Incognito Window 1** (User A)
   - Go to `http://localhost:3000`
   - Sign up as `user_a@test.com`
   - Upload an invoice (e.g., "Invoice A")

2. Open **Incognito Window 2** (User B)
   - Go to `http://localhost:3000`
   - Sign up as `user_b@test.com`
   - Upload a *different* invoice (e.g., "Invoice B")

## Step 2: Verify Isolation

1. **Check User A's List**:
   - In Window 1, go to "Invoice List".
   - You should **ONLY** see "Invoice A".
   - You should **NOT** see "Invoice B".

2. **Check User B's List**:
   - In Window 2, go to "Invoice List".
   - You should **ONLY** see "Invoice B".

## Step 3: Verify Backend Security (The "Hacker" Test)

Try to access User A's invoice using User B's account.

1. In Window 1 (User A), click "Edit" on an invoice.
2. Copy the **Invoice ID** from the URL or console (e.g., `e5dfa...`).
3. In Window 2 (User B), try to manually call the API (using curl or Postman):
   
   ```bash
   # You need User B's token for this, which is hard to get manually, 
   # but the app handles it.
   ```
   
   **Easier Test**: 
   - If you try to view an invoice ID that doesn't belong to you, the API will return `403 Access Denied` or `404 Not Found`.

---

## 🧠 What This Means for Business

1. **Security**: You can now host this on a public server (Railway).
2. **Multi-Tenancy**: You can have 10 different clients testing at the same time.
3. **Data Privacy**: Client A (Restaurant) won't see Client B's (Electronics) invoices.

---

## 📝 Next Feature to Build (The "Sticky" HSN)

To make this sellable, we should build **"Smart HSN Learning"**:

1. **Scenario**: App predicts HSN `1234` (18%).
2. **User Action**: User edits it to `5678` (12%).
3. **System Action**: We save this preference:
   - `Vendor: ABC Corp` + `Item: Widget` = `HSN 5678`
4. **Next Time**: When `ABC Corp` sends an invoice for `Widget`, we auto-apply `5678`.

**Shall we add this to the roadmap?**
