import requests
import hashlib
import base64
from datetime import datetime
from src.config.settings import settings

class SelcomPay:
    def __init__(self):
        self.base_url = "https://apigateway.selcom.co.tz"
        self.vendor_id = getattr(settings, 'SELCOM_VENDOR_ID', 'your-vendor-id')
        self.api_key = getattr(settings, 'SELCOM_API_KEY', 'your-api-key')

    def generate_signature(self, data: dict, timestamp: str):
        data_string = ''.join([f"{k}={v}" for k, v in sorted(data.items())])
        sign_string = f"timestamp={timestamp}&{data_string}"
        signature = hmac.new(self.api_key.encode(), sign_string.encode(), hashlib.sha256).digest()
        return base64.b64encode(signature).decode()

    def create_order(self, amount: float, order_id: str, buyer_email: str, buyer_name: str, buyer_phone: str):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {
            "vendor": self.vendor_id,
            "amount": str(amount),
            "order_id": order_id,
            "buyer_email": buyer_email,
            "buyer_name": buyer_name,
            "buyer_phone": buyer_phone,
            "currency": "TZS",
            "payment_methods": "MOBILE_MONEY,CARD"
        }
        signature = self.generate_signature(data, timestamp)
        headers = {
            "Authorization": f"SELCOM {self.vendor_id}:{signature}",
            "Timestamp": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.base_url}/v1/checkout/create-order", json=data, headers=headers)
        return response.json()

    def check_order_status(self, order_id: str):
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        data = {"order_id": order_id, "vendor": self.vendor_id}
        signature = self.generate_signature(data, timestamp)
        headers = {
            "Authorization": f"SELCOM {self.vendor_id}:{signature}",
            "Timestamp": timestamp,
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.base_url}/v1/checkout/order-status", json=data, headers=headers)
        return response.json()

selcom_pay = SelcomPay()
