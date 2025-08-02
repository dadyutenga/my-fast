from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AuditLogBase(BaseModel):
    user_id: int
    entity_type: str
    entity_id: int
    action: str
    details: Optional[str] = None

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogInDB(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
