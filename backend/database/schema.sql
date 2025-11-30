-- Database Schema for GST Automation (PostgreSQL)

-- 1. Users Table (Managed by Supabase Auth usually, but we'll define a reference)
-- We will link invoices to the 'auth.users' table provided by Supabase
-- For local development/testing without Supabase, we can use a simple users table

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    gstin TEXT, -- User's own GSTIN
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Invoices Table
-- Stores the main invoice details (formerly the top-level JSON fields)
CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE, -- Link to user
    
    -- File Details
    file_path TEXT NOT NULL, -- Path in Storage Bucket (e.g., "user_123/invoice_abc.pdf")
    file_name TEXT NOT NULL,
    file_size INTEGER,
    content_type TEXT, -- pdf, image/png, etc.
    
    -- Extracted Data
    invoice_number TEXT,
    invoice_date DATE,
    invoice_type TEXT CHECK (invoice_type IN ('purchase', 'sales')),
    vendor_gstin TEXT,
    vendor_name TEXT,
    
    -- Financials
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    cgst_amount DECIMAL(12, 2) DEFAULT 0.00,
    sgst_amount DECIMAL(12, 2) DEFAULT 0.00,
    igst_amount DECIMAL(12, 2) DEFAULT 0.00,
    gst_rate DECIMAL(5, 2), -- Main tax rate detected
    
    -- Metadata
    status TEXT DEFAULT 'processed', -- processed, failed, pending_review
    ocr_confidence DECIMAL(5, 2),
    is_gstr3b_generated BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Invoice Line Items Table
-- Stores individual items from the invoice (formerly 'line_items' array)
CREATE TABLE IF NOT EXISTS invoice_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    invoice_id UUID REFERENCES invoices(id) ON DELETE CASCADE,
    
    description TEXT,
    hsn_code TEXT,
    quantity DECIMAL(10, 2) DEFAULT 1.0,
    rate DECIMAL(12, 2),
    amount DECIMAL(12, 2),
    gst_rate DECIMAL(5, 2),
    
    confidence_score DECIMAL(5, 2) -- HSN matching confidence
);

-- 4. GSTR-3B Reports Table
-- Stores generated reports history
CREATE TABLE IF NOT EXISTS gstr3b_reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL,
    gstin TEXT NOT NULL,
    
    -- Stored as JSONB for flexibility since report structure is complex
    report_data JSONB NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_invoices_user_id ON invoices(user_id);
CREATE INDEX idx_invoices_date ON invoices(invoice_date);
CREATE INDEX idx_invoices_vendor_gstin ON invoices(vendor_gstin);
