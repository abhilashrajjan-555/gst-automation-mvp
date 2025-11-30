/**
 * Type definitions for GST Automation MVP
 * Matches backend API response structures
 */

export type InvoiceType = 'sales' | 'purchase';

export interface Invoice {
  invoice_number: string;
  invoice_date: string;
  invoice_type: InvoiceType;
  total_amount: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  taxable_amount: number;
  vendor_name?: string;
  customer_name?: string;
  gstin?: string;
  items?: InvoiceItem[];
  confidence?: number;
  file_path?: string;
  processing_time?: number;
}

export interface InvoiceItem {
  description: string;
  hsn_code: string;
  quantity: number;
  rate: number;
  amount: number;
  tax_rate: number;
  cgst?: number;
  sgst?: number;
  igst?: number;
}

export interface DashboardStats {
  total_invoices: number;
  sales_count: number;
  purchase_count: number;
  total_amount: number;
  total_tax: number;
  avg_processing_confidence: number;
}

export interface GSTR3BData {
  gstin: string;
  month: number;
  year: number;
  legal_name?: string;
  trade_name?: string;
  filing_date?: string;

  // Table 3.1 - Outward taxable supplies
  outward_taxable_supplies: {
    total_taxable_value: number;
    integrated_tax: number;
    central_tax: number;
    state_ut_tax: number;
  };

  // Table 3.2 - Inward supplies liable to reverse charge
  inward_reverse_charge: {
    total_taxable_value: number;
    integrated_tax: number;
    central_tax: number;
    state_ut_tax: number;
  };

  // Table 4 - Eligible ITC
  eligible_itc: {
    import_of_goods: {
      integrated_tax: number;
    };
    import_of_services: {
      integrated_tax: number;
    };
    inward_reverse_charge: {
      integrated_tax: number;
      central_tax: number;
      state_ut_tax: number;
    };
    inward_supplies: {
      integrated_tax: number;
      central_tax: number;
      state_ut_tax: number;
    };
    all_itc: {
      integrated_tax: number;
      central_tax: number;
      state_ut_tax: number;
    };
  };

  // Table 5 - Exempt, Nil rated and Non-GST supplies
  exempt_supplies?: {
    inter_state: number;
    intra_state: number;
  };

  // Interest and late fee
  interest?: {
    integrated_tax: number;
    central_tax: number;
    state_ut_tax: number;
  };
}

// API Response types
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  data: {
    invoice_number: string;
    invoice_date: string;
    invoice_type: InvoiceType;
    total_amount: number;
    confidence: number;
    items?: InvoiceItem[];
  };
}

export interface InvoicesResponse {
  success: boolean;
  count: number;
  invoices: Invoice[];
}

export interface StatsResponse {
  success: boolean;
  stats: DashboardStats;
}

export interface GSTR3BResponse {
  success: boolean;
  message: string;
  data: GSTR3BData;
  file_path?: string;
}
