from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PaymentRequest(BaseModel):
    amount: float = Field(..., ge=0.0)
    order_id: str
    buyer_email: str
    buyer_name: str
    buyer_phone: str

class PaymentStatus(BaseModel):
    order_id: str
