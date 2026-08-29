"use client"
import { useEffect, useState } from 'react'

export default function AgentActivity() {
  const [activity, setActivity] = useState<any[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/agent/activity')
      .then(r => r.json())
      .then(d => setActivity(d))
      .catch(e => console.error(e))
  }, [])

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Live Agent Activity</h1>
      <div className="space-y-4">
        {activity.map((a, i) => (
          <div key={i} className="bg-white p-4 rounded shadow border-l-4 border-blue-500 flex flex-col">
            <div className="flex justify-between mb-2">
              <span className="font-bold text-gray-800">{a.decision}</span>
              <span className="font-mono text-sm text-gray-500">{a.transaction_id}</span>
            </div>
            <p className="text-gray-600">{a.reasoning}</p>
            <span className="text-xs text-gray-400 mt-2">{new Date(a.timestamp).toLocaleString()}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
