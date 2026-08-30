'use client'

import { useEffect, useState } from 'react'
import { BrainCircuit, ShieldAlert, Activity, CheckCircle2 } from 'lucide-react'

export default function AgentActivity() {
  const [activities, setActivities] = useState<any[]>([])

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/agent/activity')
      .then(res => res.json())
      .then(data => setActivities(data))
  }, [])

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Live Agent Activity</h1>
        <p className="text-slate-500 mt-1">Real-time AI decisions and recovery outcomes</p>
      </div>

      <div className="space-y-4">
        {activities.map((act, i) => (
          <div key={i} className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden p-5 flex flex-col md:flex-row gap-6">
            <div className="flex-1 space-y-4">
              {/* AI DECISION */}
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 flex items-center gap-1">
                  <BrainCircuit size={12}/> AI Recommendation
                </div>
                <div className="font-bold text-slate-800 text-lg mb-1">{act.decision}</div>
                <div className="text-sm text-slate-600">"{act.reasoning}"</div>
                
                <div className="flex gap-4 mt-3">
                  <div className="bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-100 text-sm flex items-center gap-2">
                    <span className="text-slate-400">Recovery Score:</span> 
                    <span className="font-bold text-slate-700">{act.recovery_score}</span>
                  </div>
                  <div className="bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-100 text-sm flex items-center gap-2">
                    <span className="text-slate-400">Security Risk:</span> 
                    <span className={`font-bold ${act.security_risk > 70 ? 'text-red-500' : 'text-slate-700'}`}>{act.security_risk}</span>
                  </div>
                </div>
              </div>
              
              <div className="w-px h-6 bg-slate-200 ml-4"></div>
              
              {/* POLICY EVALUATION */}
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 flex items-center gap-1">
                  <ShieldAlert size={12}/> Policy Evaluation
                </div>
                <div className="flex items-center gap-3 mb-1">
                  <div className={`font-bold text-sm px-2 py-1 rounded ${act.policy_decision === 'APPROVED' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
                    {act.policy_decision}
                  </div>
                  {act.policy_decision === 'APPROVED' ? (
                    <div className="text-xs text-slate-500 font-bold">Rules Passed: {act.policy_rules}/{act.policy_rules}</div>
                  ) : (
                    <div className="text-xs text-red-500 font-bold">Reason: {act.policy_reason}</div>
                  )}
                </div>
              </div>
              
              <div className="w-px h-6 bg-slate-200 ml-4"></div>
              
              {/* FINAL ACTION */}
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Action</div>
                <div className="font-bold text-blue-700 text-sm">{act.approved_action}</div>
              </div>
              
              <div className="w-px h-6 bg-slate-200 ml-4"></div>
              
              {/* RESULT */}
              <div>
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1">Result</div>
                {act.result === 'RECOVERED' ? (
                  <div className="flex items-center gap-1 text-emerald-600 text-sm font-bold">
                    <CheckCircle2 size={16}/> ?{act.amount_recovered} RECOVERED
                  </div>
                ) : (
                  <div className="text-slate-600 text-sm font-bold">{act.result}</div>
                )}
              </div>
              
            </div>
            
            <div className="text-right">
              <div className="font-mono text-xs text-slate-400">{act.transaction_id}</div>
              <div className="text-[10px] text-slate-400 mt-1">{new Date(act.timestamp).toLocaleString()}</div>
            </div>
          </div>
        ))}
        
        {activities.length === 0 && (
          <div className="text-center p-12 bg-white rounded-xl border border-dashed border-slate-300 text-slate-500">
            No agent activity recorded yet. Run a simulation to see AI decisions.
          </div>
        )}
      </div>
    </div>
  )
}
