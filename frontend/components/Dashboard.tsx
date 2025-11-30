'use client';
import { useState, useEffect } from 'react';
import { API_URL } from '@/lib/api';

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/api/stats`)
      .then(res => res.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
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
