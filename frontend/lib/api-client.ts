/**
 * API client for communicating with FastAPI backend
 * All API calls are centralized here for maintainability
 */

import type {
  UploadResponse,
  InvoicesResponse,
  StatsResponse,
  GSTR3BResponse,
  InvoiceType,
} from '@/types/invoice';
import { supabase } from '@/lib/supabase';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get auth headers from current Supabase session
 */
async function getAuthHeaders(): Promise<Record<string, string>> {
  const { data: { session } } = await supabase.auth.getSession();
  const token = session?.access_token;
  if (!token) {
    throw new Error('Authentication required. Please sign in.');
  }
  return { 'Authorization': `Bearer ${token}` };
}

/**
 * Helper function to handle API responses
 * Throws error if response is not ok
 */
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({
      detail: 'An unknown error occurred',
    }));
    throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
  }
  return response.json();
}

/**
 * Upload and process an invoice
 */
export async function uploadInvoice(
  file: File,
  invoiceType: InvoiceType
): Promise<UploadResponse> {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append('file', file);
  formData.append('invoice_type', invoiceType);

  const response = await fetch(`${API_BASE_URL}/api/upload-invoice`, {
    method: 'POST',
    headers,
    body: formData,
  });

  return handleResponse<UploadResponse>(response);
}

/**
 * Fetch all processed invoices for the authenticated user
 */
export async function fetchInvoices(): Promise<InvoicesResponse> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/api/invoices`, { headers });
  return handleResponse<InvoicesResponse>(response);
}

/**
 * Fetch dashboard statistics for the authenticated user
 */
export async function fetchStats(): Promise<StatsResponse> {
  const headers = await getAuthHeaders();
  const response = await fetch(`${API_BASE_URL}/api/stats`, { headers });
  return handleResponse<StatsResponse>(response);
}

/**
 * Generate GSTR-3B monthly return
 */
export async function generateGSTR3B(
  gstin: string,
  month: number,
  year: number
): Promise<GSTR3BResponse> {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append('gstin', gstin);
  formData.append('month', month.toString());
  formData.append('year', year.toString());

  const response = await fetch(`${API_BASE_URL}/api/generate-gstr3b`, {
    method: 'POST',
    headers,
    body: formData,
  });

  return handleResponse<GSTR3BResponse>(response);
}

/**
 * Health check endpoint (no auth needed)
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  return handleResponse<{ status: string }>(response);
}
