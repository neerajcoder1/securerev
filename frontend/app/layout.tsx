import './globals.css'
import Sidebar from '../components/Sidebar'

export const metadata = {
  title: 'SecureRev',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="flex bg-gray-50 text-gray-900">
        <Sidebar />
        <main className="flex-1 p-8 overflow-y-auto h-screen">
          {children}
        </main>
      </body>
    </html>
  )
}
