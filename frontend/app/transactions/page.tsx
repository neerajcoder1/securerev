'use client'

import { useEffect, useState } from 'react'
import { ShieldAlert, ShieldCheck, Activity, BrainCircuit, CheckCircle2, XCircle, Clock } from 'lucide-react'

export default function Transactions() {
  const [transactions, setTransactions] = useState<any[]>([])
  const [selectedTxn, setSelectedTxn] = useState<string | null>(null)
  const [txnDetails, setTxnDetails] = useState<any>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/transactions')
      .then(res => res.json())
      .then(data => setTransactions(data))
  }, [])

  const loadDetails = async (id: string) => {
    if (selectedTxn === id) {
      setSelectedTxn(null)
      return
    }
    const res = await fetch(`http://localhost:8000/api/v1/transactions/${id}`)
    const data = await res.json()
    setTxnDetails(data)
    setSelectedTxn(id)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RECOVERED': return 'bg-green-100 text-green-700 border-green-200'
      case 'FAILED': return 'bg-red-100 text-red-700 border-red-200'
      case 'ESCALATED': return 'bg-amber-100 text-amber-700 border-amber-200'
      default: return 'bg-slate-100 text-slate-700 border-slate-200'
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case 'HIGH': return 'text-red-600 font-bold'
      case 'MEDIUM': return 'text-amber-600 font-bold'
      case 'LOW': return 'text-green-600 font-bold'
      default: return 'text-slate-600'
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6 pb-20">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Transaction Explorer</h1>
        <p className="text-slate-500 mt-1">Audit trail and AI recovery decisions</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-x-auto">
        <table className="w-full text-left">
          <thead className="bg-slate-50 border-b border-slate-200 text-sm font-semibold text-slate-600">
            <tr>
              <th className="py-4 px-6">ID</th>
              <th className="py-4 px-6">Source</th>
              <th className="py-4 px-6">Amount</th>
              <th className="py-4 px-6">Failure Reason</th>
              <th className="py-4 px-6">Status</th>
              <th className="py-4 px-6">Risk Level</th>
              <th className="py-4 px-6 whitespace-nowrap">AI Decision</th>
              <th className="py-4 px-6 whitespace-nowrap">Policy</th>
              <th className="py-4 px-6 whitespace-nowrap">Final Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-sm">
            {transactions.map((t) => (
              <React.Fragment key={t.id}>
                <tr 
                  className={`hover:bg-slate-50 cursor-pointer transition-colors ${selectedTxn === t.id ? 'bg-blue-50/50' : ''}`}
                  onClick={() => loadDetails(t.id)}
                >
                  <td className="py-4 px-6 font-mono text-slate-600">{t.id}</td>
                  <td className="py-4 px-6 font-semibold text-xs text-slate-500 uppercase">{t.source}</td>
                  <td className="py-4 px-6 font-medium text-slate-800">₹{t.amount}</td>
                  <td className="py-4 px-6 text-red-500 max-w-sm truncate" title={t.failure_reason}>{t.failure_reason}</td>
                  <td className="py-4 px-6">
                    <span className={`px-2.5 py-1 rounded-md text-xs font-bold border ${getStatusColor(t.status)}`}>
                      {t.status}
                    </span>
                  </td>
                  <td className={`py-4 px-6 ${getRiskColor(t.risk_assessment?.risk_level)}`}>
                    {t.risk_assessment?.risk_level || 'N/A'}
                  </td>
                  <td className="py-4 px-6 text-slate-700 font-medium whitespace-nowrap">
                    {t.agent_decision?.decision || 'N/A'}
                  </td>
                </tr>
                {selectedTxn === t.id && txnDetails && (
                  <tr>
                    <td colSpan={9} className="p-0 border-b-2 border-blue-100 bg-slate-50/50">
                      <div className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        
                        
                        {/* 0. Payment Provider */}
                        <div className="bg-slate-800 p-5 rounded-lg border border-slate-700 shadow-sm text-white lg:col-span-3">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                              <div className="bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded">RAZORPAY</div>
                              <span className="text-slate-300 text-sm tracking-widest font-mono">ENVIRONMENT: TEST MODE</span>
                            </div>

                            <div className="text-right flex gap-6 text-sm">
                              <div><span className="text-slate-400">Order ID:</span> <span className="font-mono text-blue-300">{txnDetails.razorpay_order_id || 'N/A'}</span></div>
                              <div><span className="text-slate-400">Payment ID:</span> <span className="font-mono text-blue-300">{txnDetails.razorpay_payment_id || 'N/A'}</span></div>
                            </div>
                          </div>
                          
                          <div className="mt-4 pt-4 border-t border-slate-700 flex flex-col">
                            <span className="text-xs text-slate-400 uppercase tracking-widest font-bold mb-1">Full Failure Reason</span>
                            <span className="text-red-400">{txnDetails.failure_reason}</span>
                          </div>
                        </div>

                        {/* 1. Security Analysis */}
                        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex items-center gap-2 text-slate-800 font-bold mb-4">
                            <ShieldAlert className="text-blue-500" size={20}/> Security Analysis
                          </div>
                          <div className="flex justify-between items-end mb-4">
                            <div>
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold">Risk Level</div>
                              <div className={`text-xl ${getRiskColor(txnDetails.risk_assessment?.risk_level)}`}>{txnDetails.risk_assessment?.risk_level}</div>
                            </div>
                            <div className="text-right">
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold">Score</div>
                              <div className="text-xl font-bold text-slate-800">{txnDetails.risk_assessment?.risk_score}/100</div>
                            </div>
                          </div>
                          <div className="space-y-2">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-2">Signals</div>
                            {txnDetails.risk_assessment?.signals?.map((sig: string, i: number) => (
                              <div key={i} className={`text-sm flex items-start gap-2 ${sig.startsWith('✓') ? 'text-green-700' : 'text-red-600'}`}>
                                <span>{sig}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        {/* 2. Recovery Analysis */}
                        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex items-center gap-2 text-slate-800 font-bold mb-4">
                            <Activity className="text-green-500" size={20}/> Recovery Analysis
                          </div>
                          <div className="flex justify-between items-end mb-6">
                            <div>
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold">Recovery Score</div>
                              <div className="text-2xl font-bold text-slate-800">{txnDetails.recovery_assessment?.recovery_score}/100</div>
                            </div>
                            <div className="text-right">
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold">Probability</div>
                              <div className="text-2xl font-bold text-green-600">{(txnDetails.recovery_assessment?.expected_recovery_probability * 100).toFixed(0)}%</div>
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Recommended Strategy</div>
                            <div className="text-sm font-bold text-slate-700 bg-slate-100 p-2 rounded inline-block">
                              {txnDetails.recovery_assessment?.recommended_action}
                            </div>
                          </div>
                        </div>

                        {/* 3. AI Decision */}
                        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex items-center gap-2 text-slate-800 font-bold mb-4">
                            <BrainCircuit className="text-purple-500" size={20}/> AI Decision
                          </div>
                          <div className="mb-4">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Action</div>
                            <div className="text-sm font-bold text-purple-700 bg-purple-50 p-2 rounded inline-block border border-purple-100">
                              {txnDetails.agent_decision?.decision}
                            </div>
                          </div>
                          <div className="mb-4">
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Confidence</div>
                            <div className="text-sm font-bold text-slate-800">
                              {(txnDetails.agent_decision?.confidence * 100).toFixed(1)}%
                            </div>
                          </div>
                          <div>
                            <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-1">Reasoning</div>
                            <div className="text-sm text-slate-600 italic">
                              "{txnDetails.agent_decision?.reasoning}"
                            </div>
                          </div>
                        </div>

                        {/* 4. Policy Evaluation */}
                        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm lg:col-span-2">
                          <div className="flex items-center gap-2 text-slate-800 font-bold mb-4">
                            <ShieldCheck className="text-amber-500" size={20}/> Deterministic Policy Engine
                          </div>
                          <div className="grid grid-cols-2 gap-6">
                            <div>
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-3">Rule Evaluation</div>
                              <div className="space-y-2">
                                {txnDetails.recovery_action?.policy_evaluation?.map((rule: any, i: number) => (
                                  <div key={i} className="flex items-center gap-2 text-sm">
                                    {rule.passed ? <CheckCircle2 size={16} className="text-green-500"/> : <XCircle size={16} className="text-red-500"/>}
                                    <span className={rule.passed ? 'text-slate-700' : 'text-red-700 font-medium'}>{rule.rule}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                            <div className="border-l border-slate-100 pl-6">
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-2">Final Action</div>
                              <div className="text-sm font-bold text-slate-800 mb-4">{txnDetails.recovery_action?.action_type}</div>
                              
                              <div className="text-xs text-slate-500 uppercase tracking-wider font-bold mb-2">Result</div>
                              <div className={`inline-block px-3 py-1 rounded-md text-xs font-bold border ${getStatusColor(txnDetails.status)}`}>
                                {txnDetails.status}
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* 5. Audit Timeline */}
                        <div className="bg-white p-5 rounded-lg border border-slate-200 shadow-sm">
                          <div className="flex items-center gap-2 text-slate-800 font-bold mb-4">
                            <Clock className="text-slate-500" size={20}/> Audit Timeline
                          </div>
                          <div className="space-y-4 max-h-64 overflow-y-auto pr-2">
                            {txnDetails.audit_logs?.map((log: any, i: number) => (
                              <div key={i} className="flex gap-3 text-sm relative">
                                <div className="flex flex-col items-center">
                                  <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5"></div>
                                  {i !== txnDetails.audit_logs.length - 1 && <div className="w-px h-full bg-slate-200 mt-1"></div>}
                                </div>
                                <div className="pb-4">
                                  <div className="text-xs text-slate-400 font-mono mb-1">
                                    {new Date(log.timestamp).toLocaleTimeString()}
                                  </div>
                                  <div className="font-semibold text-slate-700 text-xs">
                                    {log.event_type.replace(/_/g, ' ')}
                                  </div>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
import React from 'react'
