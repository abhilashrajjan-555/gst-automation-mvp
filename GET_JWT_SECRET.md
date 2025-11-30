# Get Supabase JWT Secret

## Where to Find It:

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **API**
4. Scroll down to **JWT Settings**
5. Copy the **JWT Secret** (it's a long string)

## Add to Backend .env:

Open `backend/.env` and add this line:

```
SUPABASE_JWT_SECRET=your-jwt-secret-here
```

**Important**: This is different from the anon key. It's used to verify JWT tokens on the backend.

## Example:

Your `.env` should look like:

```
SUPABASE_URL=https://ferpnklaqqvfqqvmgyor.supabase.co
SUPABASE_KEY=eyJhbGci...
SUPABASE_JWT_SECRET=tvUprPSwu9WhCgVoYaQBk36K0TiKoqdZ4TDXYL1IT1FMbxfiZmwebzq+huSm4yWDQVpTY2rD3BwiUcWQPtGRhw==
```

---

**After adding it, restart the backend server.**
