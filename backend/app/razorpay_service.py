import razorpay
import hmac
import hashlib
from app.config import settings

class RazorpayClient:
    def __init__(self):
        self.key_id = settings.RAZORPAY_KEY_ID
        self.key_secret = settings.RAZORPAY_KEY_SECRET
        self.webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        
        if self.key_id and self.key_secret:
            self.client = razorpay.Client(auth=(self.key_id, self.key_secret))
        else:
            self.client = None

    def create_order(self, amount: float, currency: str = "INR", receipt: str = None) -> dict:
        """Create a Razorpay order. Amount is in standard unit (e.g. INR), we multiply by 100 for paise."""
        if not self.client:
            raise Exception("Razorpay credentials not configured")
            
        data = {
            "amount": int(amount * 100),
            "currency": currency,
            "receipt": receipt or "receipt_test"
        }
        order = self.client.order.create(data=data)
        return order

    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify the signature returned by checkout."""
        if not self.key_secret:
            return False
            
        generated_signature = hmac.new(
            self.key_secret.encode('utf-8'),
            f"{order_id}|{payment_id}".encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(generated_signature, signature)

    def verify_webhook_signature(self, payload: str, signature: str) -> bool:
        """Verify webhook signature."""
        if not self.webhook_secret:
            return False
            
        generated_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(generated_signature, signature)

razorpay_client = RazorpayClient()
