'use client';
import { useState } from 'react';
import { API_URL } from '@/lib/api';

export default function Reconciliation() {
    const [gstr2aFile, setGstr2aFile] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [reconciliationResult, setReconciliationResult] = useState<any>(null);

    const handleUpload = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!gstr2aFile) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', gstr2aFile);

        try {
            const response = await fetch(`${API_URL}/api/reconcile-gstr2a`, {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            setReconciliationResult(data);
        } catch (error) {
            console.error('Upload failed:', error);
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-4">GSTR-2A Reconciliation</h2>
                <p className="text-sm text-gray-600 mb-6">
                    Upload your GSTR-2A data (downloaded from GST Portal) to reconcile with your uploaded invoices.
                </p>

                <form onSubmit={handleUpload} className="space-y-4">
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:bg-gray-50">
                        <input
                            type="file"
                            onChange={(e) => setGstr2aFile(e.target.files?.[0] || null)}
                            className="hidden"
                            id="gstr2a-upload"
                            accept=".xlsx,.xls,.json"
                        />
                        <label htmlFor="gstr2a-upload" className="cursor-pointer flex flex-col items-center">
                            <svg className="w-12 h-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                            </svg>
                            <span className="text-blue-600 font-medium">
                                {gstr2aFile ? gstr2aFile.name : 'Click to upload GSTR-2A file'}
                            </span>
                            <p className="text-gray-500 text-sm mt-1">Excel or JSON format</p>
                        </label>
                    </div>

                    <button
                        type="submit"
                        disabled={!gstr2aFile || uploading}
                        className={`w-full py-2 px-4 rounded-md text-white font-medium ${!gstr2aFile || uploading ? 'bg-gray-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
                            }`}
                    >
                        {uploading ? 'Processing...' : 'Reconcile'}
                    </button>
                </form>
            </div>

            {reconciliationResult && (
                <div className="bg-white rounded-lg shadow p-6">
                    <h3 className="text-lg font-bold mb-4">Reconciliation Results</h3>

                    <div className="grid grid-cols-3 gap-4 mb-6">
                        <div className="bg-green-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-600">Matched</p>
                            <p className="text-2xl font-bold text-green-600">{reconciliationResult.matched || 0}</p>
                        </div>
                        <div className="bg-yellow-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-600">Missing in Portal</p>
                            <p className="text-2xl font-bold text-yellow-600">{reconciliationResult.missing_in_portal || 0}</p>
                        </div>
                        <div className="bg-red-50 p-4 rounded-lg">
                            <p className="text-sm text-gray-600">Amount Mismatch</p>
                            <p className="text-2xl font-bold text-red-600">{reconciliationResult.amount_mismatch || 0}</p>
                        </div>
                    </div>

                    {reconciliationResult.details && reconciliationResult.details.length > 0 && (
                        <div className="overflow-x-auto">
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Invoice #</th>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Vendor GSTIN</th>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Your Amount</th>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Portal Amount</th>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {reconciliationResult.details.map((item: any, idx: number) => (
                                        <tr key={idx} className={item.status === 'matched' ? 'bg-green-50' : item.status === 'mismatch' ? 'bg-red-50' : 'bg-yellow-50'}>
                                            <td className="px-4 py-2 text-sm">{item.invoice_number}</td>
                                            <td className="px-4 py-2 text-sm">{item.vendor_gstin}</td>
                                            <td className="px-4 py-2 text-sm">₹{item.your_amount?.toLocaleString('en-IN')}</td>
                                            <td className="px-4 py-2 text-sm">₹{item.portal_amount?.toLocaleString('en-IN') || 'N/A'}</td>
                                            <td className="px-4 py-2 text-sm">
                                                <span className={`px-2 py-1 text-xs rounded-full ${item.status === 'matched' ? 'bg-green-100 text-green-800' :
                                                    item.status === 'mismatch' ? 'bg-red-100 text-red-800' :
                                                        'bg-yellow-100 text-yellow-800'
                                                    }`}>
                                                    {item.status}
                                                </span>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            )}

            <div className="bg-blue-50 border-l-4 border-blue-400 p-4">
                <div className="flex">
                    <div className="flex-shrink-0">
                        <svg className="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                        </svg>
                    </div>
                    <div className="ml-3">
                        <h3 className="text-sm font-medium text-blue-800">How to download GSTR-2A</h3>
                        <div className="mt-2 text-sm text-blue-700">
                            <ol className="list-decimal list-inside space-y-1">
                                <li>Login to GST Portal (https://www.gst.gov.in)</li>
                                <li>Go to Returns → GSTR-2A</li>
                                <li>Select the tax period (month/year)</li>
                                <li>Click "Download" and save as Excel</li>
                                <li>Upload the file here</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
