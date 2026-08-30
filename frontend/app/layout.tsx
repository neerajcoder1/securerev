import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Sidebar from '../components/Sidebar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'SecureRev | Merchant Dashboard',
  description: 'Autonomous Secure Revenue Recovery Agent',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-50 text-slate-900`}>
        <div className="flex h-screen overflow-hidden">
          <Sidebar />
          <div className="flex-1 flex flex-col overflow-y-auto">
            <header className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center sticky top-0 z-10">
              <div>
                <h2 className="text-lg font-bold text-slate-800">Acme Corp</h2>
                <p className="text-xs text-slate-500 font-medium">MERCHANT_ID: M_8492</p>
              </div>
              <div className="flex items-center gap-3">
                <span className="px-3 py-1 bg-amber-100 text-amber-800 text-xs font-bold rounded-full tracking-wider border border-amber-200">
                  RAZORPAY TEST MODE
                </span>
                <div className="h-8 w-8 bg-slate-200 rounded-full flex items-center justify-center text-slate-600 font-bold text-sm">
                  AC
                </div>
              </div>
            </header>
            <main className="flex-1 p-8">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  )
}
