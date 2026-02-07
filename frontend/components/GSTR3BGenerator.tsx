'use client';
import { useState } from 'react';
import { supabase } from '@/lib/supabase';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function GSTR3BGenerator() {
  const [gstin, setGstin] = useState('29AABCT1234A1Z5');
  const [month, setMonth] = useState('12');
  const [year, setYear] = useState('2024');
  const [generating, setGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);

    const { data: { session } } = await supabase.auth.getSession();
    const token = session?.access_token;

    if (!token) {
      setResult({ success: false, error: 'Authentication required' });
      setGenerating(false);
      return;
    }

    const formData = new FormData();
    formData.append('gstin', gstin);
    formData.append('month', month);
    formData.append('year', year);

    try {
      const res = await fetch(`${API_URL}/api/generate-gstr3b`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
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
              </div>
            ) : (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6">
                <p className="text-red-800 font-medium">Error: {result.error || result.detail}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
