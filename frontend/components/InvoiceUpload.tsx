'use client';
import { useState } from 'react';
import { supabase } from '@/lib/supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function InvoiceUpload() {
  const [files, setFiles] = useState<FileList | null>(null);
  const [invoiceType, setInvoiceType] = useState('purchase');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length === 0) return;

    setUploading(true);
    setResult(null);

    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    if (!token) {
      setResult({ success: false, message: 'Authentication required' });
      setUploading(false);
      return;
    }

    const formData = new FormData();
    formData.append('invoice_type', invoiceType);

    // Determine if bulk or single upload
    const isBulk = files.length > 1;
    const endpoint = isBulk ? `${API_URL}/api/upload-bulk` : `${API_URL}/api/upload-invoice`;

    if (isBulk) {
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }
    } else {
      formData.append('file', files[0]);
    }

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Upload failed:', error);
      setResult({ success: false, message: 'Upload failed. Please try again.' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Upload Invoices</h2>

      <form onSubmit={handleUpload} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Invoice Type
          </label>
          <select
            value={invoiceType}
            onChange={(e) => setInvoiceType(e.target.value)}
            className="w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="purchase">Purchase Invoice (Input Tax Credit)</option>
            <option value="sales">Sales Invoice (Outward Supply)</option>
          </select>
        </div>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50 transition-colors">
          <input
            type="file"
            multiple
            onChange={(e) => setFiles(e.target.files)}
            className="hidden"
            id="file-upload"
            accept=".pdf,.jpg,.jpeg,.png,.docx,.doc,.xlsx,.xls"
          />
          <label
            htmlFor="file-upload"
            className="cursor-pointer flex flex-col items-center"
          >
            <svg className="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <span className="text-blue-600 font-medium hover:text-blue-500">
              {files ? `${files.length} file(s) selected` : 'Click to select files'}
            </span>
            <p className="text-gray-500 text-sm mt-1">
              PDF, JPG, PNG, Word, or Excel
            </p>
          </label>
        </div>

        {files && (
          <div className="text-sm text-gray-600">
            Selected: {Array.from(files).map(f => f.name).join(', ')}
          </div>
        )}

        <button
          type="submit"
          disabled={!files || uploading}
          className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
            ${!files || uploading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700 focus:ring-2 focus:ring-offset-2 focus:ring-blue-500'}`}
        >
          {uploading ? 'Processing...' : `Upload & Process ${files && files.length > 1 ? `(${files.length})` : ''}`}
        </button>
      </form>

      {result && (
        <div className={`mt-6 p-4 rounded-md ${result.success ? 'bg-green-50' : 'bg-red-50'}`}>
          <div className="flex">
            <div className="flex-shrink-0">
              {result.success ? (
                <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              )}
            </div>
            <div className="ml-3">
              <h3 className={`text-sm font-medium ${result.success ? 'text-green-800' : 'text-red-800'}`}>
                {result.message || (result.success ? 'Upload successful!' : 'Upload failed')}
              </h3>

              {result.success && (
                <p className="mt-1 text-sm text-green-700">
                  ✅ Invoice processed! Go to the <strong>Invoice List</strong> tab to view it.
                </p>
              )}

              {/* Bulk Upload Summary */}
              {result.summary && (
                <div className="mt-2 text-sm text-green-700">
                  <p>Total: {result.summary.total}</p>
                  <p>Success: {result.summary.success}</p>
                  <p>Failed: {result.summary.failed}</p>

                  {result.results && result.results.length > 0 && (
                    <ul className="mt-2 list-disc pl-5 space-y-1">
                      {result.results.map((res: any, idx: number) => (
                        <li key={idx} className={res.success ? 'text-green-600' : 'text-red-600'}>
                          {res.filename}: {res.success ? '✅ Success' : `❌ ${res.error}`}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}

              {/* Single Upload Details */}
              {!result.summary && result.data && (
                <div className="mt-2 text-sm text-green-700">
                  <p>Invoice ID: {result.data.invoice_id}</p>
                  <p>Amount: ₹{result.data.invoice_data?.total_amount?.toLocaleString('en-IN')}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
