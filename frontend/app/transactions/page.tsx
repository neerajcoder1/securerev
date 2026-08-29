"use client"
import { useEffect, useState } from 'react'

export default function Transactions() {
  const [txns, setTxns] = useState<any[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/transactions')
      .then(r => r.json())
      .then(d => setTxns(d))
      .catch(e => console.error(e))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Transaction Explorer</h1>
      <div className="bg-white rounded shadow overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-100">
            <tr>
              <th className="p-4">ID</th>
              <th className="p-4">Amount</th>
              <th className="p-4">Failure Reason</th>
              <th className="p-4">Status</th>
              <th className="p-4">Risk Level</th>
              <th className="p-4">AI Decision</th>
            </tr>
          </thead>
          <tbody>
            {txns.map(t => (
              <tr key={t.id} className="border-t">
                <td className="p-4 font-mono text-sm">{t.id}</td>
                <td className="p-4 font-semibold">₹{t.amount}</td>
                <td className="p-4 text-red-500">{t.failure_reason}</td>
                <td className="p-4">
                  <span className={`px-2 py-1 rounded text-xs ${t.status === 'RECOVERED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {t.status}
                  </span>
                </td>
                <td className="p-4">{t.risk_assessment?.risk_level || 'N/A'}</td>
                <td className="p-4">{t.agent_decision?.decision || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
