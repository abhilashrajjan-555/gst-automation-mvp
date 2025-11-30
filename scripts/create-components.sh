#!/bin/bash

# Script to create all frontend components for GST Automation MVP
# Run this from the project root directory

cd frontend/components || exit 1

echo "Creating React components..."

# Create Dashboard.tsx
cat > Dashboard.tsx << 'DASHBOARD_EOF'
'use client';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/stats')
      .then(res => res.json())
      .then(data => {
        setStats(data.stats);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12">Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-2">GST Automation Dashboard</h2>
        <p className="text-indigo-100">Save 75% time on GST compliance</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Invoices</p>
          <p className="text-3xl font-bold text-gray-900">{stats?.total_invoices || 0}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Amount</p>
          <p className="text-3xl font-bold text-green-600">₹{(stats?.total_amount || 0).toLocaleString('en-IN')}</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <p className="text-gray-600 text-sm">Total Tax</p>
          <p className="text-3xl font-bold text-blue-600">₹{(stats?.total_tax || 0).toLocaleString('en-IN')}</p>
        </div>
      </div>
    </div>
  );
}
DASHBOARD_EOF

# Create InvoiceUpload.tsx
cat > InvoiceUpload.tsx << 'UPLOAD_EOF'
'use client';
import { useState } from 'react';

export default function InvoiceUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [type, setType] = useState('purchase');
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('invoice_type', type);

    try {
      const res = await fetch('http://localhost:8000/api/upload-invoice', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ success: false, error: 'Upload failed' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Upload Invoice</h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Invoice File (PDF, JPG, PNG)
            </label>
            <input
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none p-2.5"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Invoice Type
            </label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  value="purchase"
                  checked={type === 'purchase'}
                  onChange={(e) => setType(e.target.value)}
                  className="mr-2"
                />
                Purchase
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  value="sales"
                  checked={type === 'sales'}
                  onChange={(e) => setType(e.target.value)}
                  className="mr-2"
                />
                Sales
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={!file || uploading}
            className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            {uploading ? 'Uploading...' : 'Upload & Process'}
          </button>
        </form>

        {result && (
          <div className={`mt-6 p-4 rounded-lg ${result.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
            <p className="font-medium">{result.success ? 'Success!' : 'Error'}</p>
            <p className="text-sm mt-1">{result.message || result.error}</p>
          </div>
        )}
      </div>
    </div>
  );
}
UPLOAD_EOF

# Create InvoiceList.tsx
cat > InvoiceList.tsx << 'LIST_EOF'
'use client';
import { useState, useEffect } from 'react';

export default function InvoiceList() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/invoices')
      .then(res => res.json())
      .then(data => {
        setInvoices(data.invoices || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12">Loading invoices...</div>;

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-900">Processed Invoices</h2>
        <p className="text-sm text-gray-600 mt-1">{invoices.length} invoices found</p>
      </div>

      {invoices.length === 0 ? (
        <div className="text-center py-12 text-gray-500">
          <p>No invoices processed yet.</p>
          <p className="text-sm mt-2">Upload an invoice to get started!</p>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Invoice #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tax</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {invoices.map((inv) => (
                <tr key={inv.invoice_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{inv.invoice_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{inv.invoice_number}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${inv.invoice_type === 'sales' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                      {inv.invoice_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">₹{inv.total_amount?.toLocaleString('en-IN')}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">₹{((inv.cgst_amount || 0) + (inv.sgst_amount || 0) + (inv.igst_amount || 0)).toLocaleString('en-IN')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
LIST_EOF

# Create GSTR3BGenerator.tsx
cat > GSTR3BGenerator.tsx << 'GSTR_EOF'
'use client';
import { useState } from 'react';

export default function GSTR3BGenerator() {
  const [gstin, setGstin] = useState('29AABCT1234A1Z5');
  const [month, setMonth] = useState('12');
  const [year, setYear] = useState('2024');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);

    const formData = new FormData();
    formData.append('gstin', gstin);
    formData.append('month', month);
    formData.append('year', year);

    try {
      const res = await fetch('http://localhost:8000/api/generate-gstr3b', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ success: false, error: 'Generation failed' });
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Generate GSTR-3B Return</h2>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">GSTIN</label>
              <input
                type="text"
                value={gstin}
                onChange={(e) => setGstin(e.target.value)}
                maxLength={15}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
                placeholder="15 characters"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Month</label>
              <select
                value={month}
                onChange={(e) => setMonth(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              >
                {Array.from({ length: 12 }, (_, i) => i + 1).map((m) => (
                  <option key={m} value={m}>{m}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Year</label>
              <input
                type="number"
                value={year}
                onChange={(e) => setYear(e.target.value)}
                min="2017"
                max="2030"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={generating}
            className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400"
          >
            {generating ? 'Generating...' : 'Generate GSTR-3B'}
          </button>
        </form>

        {result && (
          <div className="mt-8">
            {result.success ? (
              <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-green-900 mb-4">GSTR-3B Generated Successfully!</h3>
                <div className="space-y-3 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Sales:</span>
                    <span className="font-medium">₹{result.data?.summary?.total_sales?.toLocaleString('en-IN') || 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Tax on Sales:</span>
                    <span className="font-medium">₹{result.data?.summary?.total_tax_on_sales?.toLocaleString('en-IN') || 0}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Net Tax Liability:</span>
                    <span className="font-medium text-indigo-600">₹{result.data?.summary?.net_tax_liability?.toLocaleString('en-IN') || 0}</span>
                  </div>
                </div>
                <p className="mt-4 text-xs text-gray-600">File saved: {result.file_path}</p>
              </div>
            ) : (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <p className="text-red-800 font-medium">Error: {result.error}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
GSTR_EOF

echo "✅ All components created successfully!"
echo ""
echo "Components created:"
echo "  - Dashboard.tsx"
echo "  - InvoiceUpload.tsx"
echo "  - InvoiceList.tsx"
echo "  - GSTR3BGenerator.tsx"
echo ""
echo "Next steps:"
echo "1. Terminal 1: cd backend && python3 api.py"
echo "2. Terminal 2: cd frontend && npm run dev"
echo "3. Open http://localhost:3000"
