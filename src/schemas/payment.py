from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentStatusEnum(str, Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class PaymentMethodEnum(str, Enum):
    selcom = "selcom"
    paypal = "paypal"
    stripe = "stripe"
    mpesa = "mpesa"

class PaymentRequest(BaseModel):
    order_id: str
    amount: float = Field(..., ge=0.0)
    currency: str = "TZS"
    method: PaymentMethodEnum
    buyer_email: Optional[str] = None
    buyer_name: Optional[str] = None
    buyer_phone: Optional[str] = None

class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatusEnum] = None
    transaction_id: Optional[str] = None

class PaymentInDB(BaseModel):
    id: int
    user_id: int
    order_id: str
    amount: float
    currency: str
    method: PaymentMethodEnum
    status: PaymentStatusEnum
    transaction_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
