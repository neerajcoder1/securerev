import Link from 'next/link'
import { LayoutDashboard, Receipt, Activity } from 'lucide-react'

export default function Sidebar() {
  return (
    <div className="w-64 bg-slate-900 text-white min-h-screen p-4">
      <div className="text-2xl font-bold mb-8 text-blue-400">SecureRev</div>
      <nav className="space-y-4">
        <Link href="/" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <LayoutDashboard size={20} /> <span>Dashboard</span>
        </Link>
        <Link href="/transactions" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <Receipt size={20} /> <span>Transactions</span>
        </Link>
        <Link href="/agent" className="flex items-center space-x-2 p-2 hover:bg-slate-800 rounded">
          <Activity size={20} /> <span>Agent Activity</span>
        </Link>
      </nav>
    </div>
  )
}
