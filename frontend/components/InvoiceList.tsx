'use client';
import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase';
import { API_URL } from '@/lib/api';

export default function InvoiceList() {
  const [invoices, setInvoices] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const [editingInvoice, setEditingInvoice] = useState<any>(null);
  const [editForm, setEditForm] = useState({
    invoice_number: '',
    invoice_date: '',
    total_amount: 0,
    gst_rate: 0
  });

  useEffect(() => {
    const fetchInvoices = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      if (!token) return;

      try {
        const res = await fetch(`${API_URL} /api/invoices`, {
          headers: {
            'Authorization': `Bearer ${token} `
          }
        });
        const data = await res.json();
        setInvoices(data.invoices || []);
      } catch (error) {
        console.error('Error fetching invoices:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchInvoices();
  }, []);

  const startEdit = (inv: any) => {
    setEditingInvoice(inv);
    setEditForm({
      invoice_number: inv.invoice_number,
      invoice_date: inv.invoice_date,
      total_amount: inv.total_amount,
      gst_rate: inv.gst_rate || 18 // Default to 18 if missing
    });
  };

  const handleSave = async () => {
    if (!editingInvoice) return;

    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    if (!token) return;

    try {
      const response = await fetch(`${API_URL} /api/invoice / ${editingInvoice.invoice_id} `, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token} `
        },
        body: JSON.stringify(editForm),
      });

      const updatedData = await response.json();

      if (updatedData.success) {
        // Update local state
        setInvoices(invoices.map(inv =>
          inv.invoice_id === editingInvoice.invoice_id ? { ...inv, ...editForm } : inv
        ));
        setEditingInvoice(null);
      }
    } catch (error) {
      console.error('Failed to save invoice', error);
      alert('Failed to save changes');
    }
  };

  const updateReconciliationStatus = async (id: string, status: string) => {
    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    if (!token) return;

    try {
      await fetch(`${API_URL} /api/invoice / ${id} `, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token} `
        },
        body: JSON.stringify({ reconciliation_status: status }),
      });
      // Optimistic update
      setInvoices(invoices.map(inv =>
        inv.invoice_id === id ? { ...inv, reconciliation_status: status } : inv
      ));
    } catch (error) {
      console.error('Failed to update status', error);
    }
  };

  if (loading) return <div className="text-center py-10">Loading invoices...</div>;

  return (
    <div className="bg-white rounded-lg shadow">
      <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Processed Invoices</h2>
          <p className="text-sm text-gray-600 mt-1">{invoices.length} invoices found</p>
        </div>
        <a
          href={`${API_URL} /api/invoices /export/excel`}
          download
          className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          Export to Excel
        </a >
      </div >

      {
        invoices.length === 0 ? (
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
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reconciliation</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
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
                    <td className="px-6 py-4 whitespace-nowrap">
                      <select
                        value={inv.reconciliation_status || 'pending'}
                        onChange={(e) => updateStatus(inv.invoice_id, e.target.value)}
                        className={`text-xs font-medium rounded-full px-2 py-1 border-0 cursor-pointer
                        ${inv.reconciliation_status === 'matched' ? 'bg-green-100 text-green-800' :
                            inv.reconciliation_status === 'mismatch' ? 'bg-red-100 text-red-800' :
                              'bg-yellow-100 text-yellow-800'}`}
                      >
                        <option value="pending">⚠️ Pending</option>
                        <option value="matched">✅ Matched</option>
                        <option value="mismatch">❌ Mismatch</option>
                      </select>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button
                        onClick={() => startEdit(inv)}
                        className="text-indigo-600 hover:text-indigo-900"
                      >
                        Edit
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )
      }

      {/* Edit Modal */}
      {
        editingInvoice && (
          <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center">
            <div className="bg-white p-8 rounded-lg shadow-xl w-96">
              <h3 className="text-lg font-bold mb-4">Edit Invoice</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Invoice Number</label>
                  <input
                    type="text"
                    value={editForm.invoice_number}
                    onChange={(e) => setEditForm({ ...editForm, invoice_number: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Date</label>
                  <input
                    type="date"
                    value={editForm.invoice_date}
                    onChange={(e) => setEditForm({ ...editForm, invoice_date: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">Total Amount</label>
                  <input
                    type="number"
                    value={editForm.total_amount}
                    onChange={(e) => setEditForm({ ...editForm, total_amount: parseFloat(e.target.value) })}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">GST Rate (%)</label>
                  <select
                    value={editForm.gst_rate}
                    onChange={(e) => setEditForm({ ...editForm, gst_rate: parseFloat(e.target.value) })}
                    className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
                  >
                    <option value={5}>5%</option>
                    <option value={12}>12%</option>
                    <option value={18}>18%</option>
                    <option value={28}>28%</option>
                  </select>
                </div>
                <div className="flex justify-end space-x-3 mt-6">
                  <button
                    onClick={() => setEditingInvoice(null)}
                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded hover:bg-gray-300"
                  >
                    Cancel
                  </button>
                  <button
                    onClick={handleSave}
                    className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        )
      }
    </div >
  );
}
