'use client'

import { useState, useEffect } from 'react'
import { ShieldCheck, AlertCircle, CreditCard, ChevronRight } from 'lucide-react'

export default function TestPayment() {
  const [amount, setAmount] = useState('2500')
  const [customer, setCustomer] = useState('Demo Customer')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const script = document.createElement('script')
    script.src = 'https://checkout.razorpay.com/v1/checkout.js'
    script.async = true
    document.body.appendChild(script)
  }, [])

  const handlePayment = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setStatus('Creating order...')
    setError(null)

    try {
      // 1. Create Order
      const orderRes = await fetch('http://localhost:8000/api/v1/payments/orders', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: parseFloat(amount), currency: 'INR', receipt: 'test_receipt_1' })
      })
      const orderData = await orderRes.json()

      if (!orderData.order_id) {
        throw new Error("Failed to create order. Check backend credentials.")
      }

      setStatus('Opening checkout...')

      // 2. Configure Razorpay
      const options = {
        key: orderData.key_id,
        amount: orderData.amount * 100,
        currency: orderData.currency,
        name: 'Acme Corp',
        description: 'SecureRev Test Transaction',
        order_id: orderData.order_id,
        handler: async function (response: any) {
          setStatus('Verifying payment...')
          try {
            const verifyRes = await fetch('http://localhost:8000/api/v1/payments/verify', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature
              })
            })
            if (verifyRes.ok) {
              setStatus('Payment verified successfully!')
              setLoading(false)
            } else {
              throw new Error("Signature verification failed")
            }
          } catch (err: any) {
            setError(err.message)
            setStatus(null)
            setLoading(false)
          }
        },
        prefill: {
          name: customer,
          email: 'demo@example.com',
          contact: '9999999999'
        },
        theme: {
          color: '#3b82f6'
        },
        modal: {
          ondismiss: function() {
            setLoading(false);
            if (status === 'Opening checkout...') {
                setStatus(null);
            }
          }
        }
      }

      const rzp = new (window as any).Razorpay(options)
      
      // Handle payment failure dynamically for local demo (bypasses webhook need)
      rzp.on('payment.failed', async function (response: any) {
        setStatus('Payment failed. Triggering SecureRev Analysis...')
        // Simulate the webhook payload hitting the backend since localhost can't receive public webhooks easily
        try {
          await fetch('http://localhost:8000/api/v1/webhooks/local-demo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              id: response.error.metadata.payment_id,
              order_id: response.error.metadata.order_id,
              amount: parseFloat(amount) * 100,
              error_description: response.error.description
            })
          })
          setStatus('SecureRev Analysis Complete. Check the Dashboard!')
          setLoading(false)
        } catch(e) {
          // If webhook mock fails, fallback message
          setStatus('Payment failed. Check dashboard for webhook ingestion (if configured).')
          setLoading(false)
        }
      })

      rzp.open()
    } catch (err: any) {
      setError(err.message)
      setLoading(false)
      setStatus(null)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-slate-800">Razorpay Test Payment</h1>
        <p className="text-slate-500 mt-1">Generate real test transactions to trigger SecureRev intelligence</p>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="bg-amber-50 border-b border-amber-100 p-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-amber-800 font-bold">
            <AlertCircle size={20} /> Environment: TEST MODE
          </div>
        </div>
        
        <div className="p-6">
          <form onSubmit={handlePayment} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Customer Name</label>
              <input 
                type="text" 
                value={customer}
                onChange={e => setCustomer(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Amount (INR)</label>
              <input 
                type="number" 
                value={amount}
                onChange={e => setAmount(e.target.value)}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                required
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading}
              className="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 rounded-lg flex items-center justify-center gap-2 transition-colors disabled:opacity-50"
            >
              <CreditCard size={20} />
              {loading ? 'Processing...' : 'Create Test Payment'}
            </button>
          </form>

          {status && (
            <div className="mt-6 p-4 bg-slate-50 border border-slate-200 rounded-lg flex items-center gap-3 text-slate-700 font-medium">
              {status.includes('Complete') || status.includes('successfully') ? (
                <ShieldCheck className="text-green-500" size={24} />
              ) : (
                <div className="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent"></div>
              )}
              {status}
            </div>
          )}

          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 font-medium text-sm">
              {error}
            </div>
          )}
        </div>
      </div>
      
      <div className="bg-slate-50 p-6 rounded-xl border border-slate-200 text-sm text-slate-600">
        <h3 className="font-bold text-slate-800 mb-2">Hackathon Demo Instructions:</h3>
        <ol className="list-decimal pl-4 space-y-1">
          <li>Enter an amount and click Create Test Payment.</li>
          <li>When the Razorpay modal opens, select a test method (e.g., Netbanking - Failed).</li>
          <li>Complete the failure flow.</li>
          <li>SecureRev will intercept the failure event, run Security/Recovery analysis, and execute the Policy Engine.</li>
          <li>Navigate to the Dashboard to see the real-time AI decision!</li>
        </ol>
      </div>
    </div>
  )
}
