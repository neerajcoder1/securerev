'use client'

import { useEffect, useState } from 'react'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts'
import { Activity, ShieldCheck, TrendingUp, AlertTriangle } from 'lucide-react'

export default function Dashboard() {
 const [metrics, setMetrics] = useState<any>(null)
 const [loading, setLoading] = useState(false)
 const [summary, setSummary] = useState<any>(null)

 const fetchMetrics = async () => {
 const res = await fetch('http://localhost:8000/api/v1/dashboard/metrics')
 const data = await res.json()
 setMetrics(data)
 }

 useEffect(() => {
 fetchMetrics()
 }, [])

 const simulate = async () => {
 setLoading(true)
 const res = await fetch('http://localhost:8000/api/v1/simulate', { method: 'POST' })
 const data = await res.json()
 await fetchMetrics()
 setSummary(data)
 setLoading(false)
 }

 if (!metrics) return <div className="flex items-center justify-center h-full"><div className="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent"></div></div>

 const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

 return (
 <div className="max-w-7xl mx-auto space-y-6">
 <div className="flex justify-between items-center">
 <div>
 <h1 className="text-3xl font-bold text-slate-800">Revenue Recovery Dashboard</h1>
 <p className="text-slate-500 mt-1">AI-driven autonomous payment recovery</p>
 </div>
 <div className="flex gap-4 items-center">
 {summary && <span className="text-sm text-green-600 font-medium">Simulation Complete ({summary.transactions_processed} Txns)</span>}
 <button 
 onClick={simulate} 
 disabled={loading}
 className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2.5 rounded-lg font-medium transition-colors disabled:opacity-50 flex items-center gap-2 shadow-sm"
 >
 {loading ? 'Simulating...' : 'Run Demo Simulation'}
 </button>
 </div>
 </div>

 <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4 ">
 <div className="p-3 bg-red-50 text-red-600 rounded-lg"><AlertTriangle size={24} /></div>
 <div>
 <div className="text-sm text-slate-500 font-medium">Revenue at Risk</div>
 <div className="text-2xl font-bold text-slate-800">₹{metrics.revenue_at_risk.toLocaleString()}</div>
 <div className="mt-2 flex flex-col gap-0.5 text-[11px]">
 <div className="text-slate-500"><span className="font-bold text-slate-700">{metrics.total_analyzed}</span> Total Transactions</div>
 <div className="text-blue-600/80"><span className="font-bold text-blue-600">{metrics.razorpay_count}</span> Razorpay Test</div>
 <div className="text-slate-400"><span className="font-bold text-slate-500">{metrics.simulated_count}</span> Simulated</div>
 </div>
 </div>
 </div>
 
 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4 ">
 <div className="p-3 bg-green-50 text-green-600 rounded-lg"><TrendingUp size={24} /></div>
 <div>
 <div className="text-sm text-slate-500 font-medium">Revenue Recovered</div>
 <div className="text-2xl font-bold text-slate-800">₹{metrics.revenue_recovered.toLocaleString()}</div>
 <div className="text-xs text-slate-400 mt-1">Legitimate payments saved</div>
 </div>
 </div>

 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4 ">
 <div className="p-3 bg-blue-50 text-blue-600 rounded-lg"><Activity size={24} /></div>
 <div>
 <div className="text-sm text-slate-500 font-medium">Recovery Rate</div>
 <div className="text-2xl font-bold text-slate-800">{metrics.recovery_rate.toFixed(1)}%</div>
 <div className="text-xs text-slate-400 mt-1">Of total at-risk revenue</div>
 </div>
 </div>

 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center gap-4 ">
 <div className="p-3 bg-amber-50 text-amber-600 rounded-lg"><ShieldCheck size={24} /></div>
 <div>
 <div className="text-sm text-slate-500 font-medium">Unsafe Prevented</div>
 <div className="text-2xl font-bold text-slate-800">{metrics.unsafe_prevented}</div>
 <div className="text-xs text-slate-400 mt-1">Escalated to human</div>
 </div>
 </div>
 </div>

 <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 lg:col-span-2">
 <h3 className="text-lg font-bold text-slate-800 mb-6">Revenue Recovery Trend</h3>
 <div className="h-72">
 <ResponsiveContainer width="100%" height="100%">
 <AreaChart data={metrics.revenue_trend}>
 <defs>
 <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
 <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
 <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
 </linearGradient>
 </defs>
 <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
 <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} dy={10} />
 <YAxis axisLine={false} tickLine={false} tick={{fill: '#64748b', fontSize: 12}} tickFormatter={(value) => `₹${value/1000}k`} dx={-10} />
 <RechartsTooltip cursor={{stroke: '#cbd5e1', strokeWidth: 1, strokeDasharray: '4 4'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
 <Area type="monotone" dataKey="value" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
 </AreaChart>
 </ResponsiveContainer>
 </div>
 </div>

 <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
 <h3 className="text-lg font-bold text-slate-800 mb-6">Security Risk Distribution</h3>
 <div className="h-72">
 <ResponsiveContainer width="100%" height="100%">
 <BarChart data={metrics.risk_distribution} layout="vertical" margin={{ top: 0, right: 0, left: 10, bottom: 0 }}>
 <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
 <XAxis type="number" hide />
 <YAxis dataKey="name" type="category" axisLine={false} tickLine={false} tick={{fill: '#475569', fontSize: 13, fontWeight: 500}} />
 <RechartsTooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}} />
 <Bar dataKey="value" radius={[0, 4, 4, 0]}>
 {metrics.risk_distribution.map((entry: any, index: number) => (
 <Cell key={`cell-${index}`} fill={entry.name === 'HIGH' ? '#ef4444' : entry.name === 'MEDIUM' ? '#f59e0b' : '#3b82f6'} />
 ))}
 </Bar>
 </BarChart>
 </ResponsiveContainer>
 </div>
 </div>
 </div>
 </div>
 )
}
