import Link from 'next/link'
import { LayoutDashboard, Receipt, Activity, CreditCard, ShieldCheck } from 'lucide-react'

export default function Sidebar() {
  const linkClass = "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-slate-400 hover:text-slate-50 hover:bg-slate-800/80 transition-all"
  
  return (
    <div className="w-64 bg-[#0f172a] text-slate-300 min-h-screen p-4 border-r border-slate-800/50 flex flex-col">
      
      <div className="flex items-center gap-2.5 mb-10 px-2 mt-2">
        <ShieldCheck size={28} className="text-slate-300" />
        <div className="text-xl font-extrabold tracking-tight text-slate-100">SecureRev</div>
      </div>
      
      <nav className="space-y-1.5 flex-1">
        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-3 mt-4">Overview</div>
        <Link href="/" className={linkClass}>
          <LayoutDashboard size={18} /> <span>Dashboard</span>
        </Link>
        <Link href="/transactions" className={linkClass}>
          <Receipt size={18} /> <span>Transactions</span>
        </Link>
        
        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-3 mt-8">Intelligence</div>
        <Link href="/agent" className={linkClass}>
          <Activity size={18} /> <span>Agent Activity</span>
        </Link>
        
        <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3 px-3 mt-8">Developer</div>
        <Link href="/test-payment" className={linkClass}>
          <CreditCard size={18} /> <span>Test Payment</span>
        </Link>
      </nav>
      

      
    </div>
  )
}
