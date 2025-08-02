from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime

class ReceiptBase(BaseModel):
    order_id: int
    items: List[Dict[str, any]]
    total: float = Field(..., ge=0.0)

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptInDB(ReceiptBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
