"use client"
import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const fetchMetrics = () => {
    fetch('http://localhost:8000/api/v1/dashboard/metrics')
      .then(r => r.json())
      .then(d => setMetrics(d))
      .catch(e => console.error(e))
  }

  useEffect(() => { fetchMetrics() }, [])

  const simulate = async () => {
    setLoading(true)
    await fetch('http://localhost:8000/api/v1/simulate', { method: 'POST' })
    fetchMetrics()
    setLoading(false)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Revenue Recovery Dashboard</h1>
        <button onClick={simulate} disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          {loading ? 'Simulating...' : 'Run Simulation'}
        </button>
      </div>
      
      {metrics ? (
        <div className="grid grid-cols-4 gap-4 mb-8">
          <div className="bg-white p-6 rounded shadow border-l-4 border-red-500">
            <div className="text-gray-500 text-sm">Revenue at Risk</div>
            <div className="text-2xl font-bold text-red-600">₹{metrics.revenue_at_risk.toLocaleString()}</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-green-500">
            <div className="text-gray-500 text-sm">Revenue Recovered</div>
            <div className="text-2xl font-bold text-green-600">₹{metrics.revenue_recovered.toLocaleString()}</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-blue-500">
            <div className="text-gray-500 text-sm">Recovery Rate</div>
            <div className="text-2xl font-bold text-blue-600">{metrics.recovery_rate.toFixed(1)}%</div>
          </div>
          <div className="bg-white p-6 rounded shadow border-l-4 border-orange-500">
            <div className="text-gray-500 text-sm">Unsafe Prevented</div>
            <div className="text-2xl font-bold text-orange-600">{metrics.unsafe_prevented}</div>
          </div>
        </div>
      ) : (
        <p>Loading metrics... Make sure backend is running.</p>
      )}
    </div>
  )
}
