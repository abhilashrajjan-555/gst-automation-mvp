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

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
 * @param file - Invoice file (PDF/JPG/PNG)
 * @param invoiceType - 'sales' or 'purchase'
 */
export async function uploadInvoice(
  file: File,
  invoiceType: InvoiceType
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('invoice_type', invoiceType);

  const response = await fetch(`${API_BASE_URL}/api/upload-invoice`, {
    method: 'POST',
    body: formData,
  });

  return handleResponse<UploadResponse>(response);
}

/**
 * Fetch all processed invoices
 */
export async function fetchInvoices(): Promise<InvoicesResponse> {
  const response = await fetch(`${API_BASE_URL}/api/invoices`);
  return handleResponse<InvoicesResponse>(response);
}

/**
 * Fetch dashboard statistics
 */
export async function fetchStats(): Promise<StatsResponse> {
  const response = await fetch(`${API_BASE_URL}/api/stats`);
  return handleResponse<StatsResponse>(response);
}

/**
 * Generate GSTR-3B monthly return
 * @param gstin - GSTIN (15 characters)
 * @param month - Month (1-12)
 * @param year - Year (YYYY)
 */
export async function generateGSTR3B(
  gstin: string,
  month: number,
  year: number
): Promise<GSTR3BResponse> {
  const formData = new FormData();
  formData.append('gstin', gstin);
  formData.append('month', month.toString());
  formData.append('year', year.toString());

  const response = await fetch(`${API_BASE_URL}/api/generate-gstr3b`, {
    method: 'POST',
    body: formData,
  });

  return handleResponse<GSTR3BResponse>(response);
}

/**
 * Health check endpoint
 */
export async function checkHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  return handleResponse<{ status: string }>(response);
}
