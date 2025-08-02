from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserActivityBase(BaseModel):
    user_id: int
    action: str
    details: Optional[str] = None

class UserActivityCreate(UserActivityBase):
    pass

class UserActivityInDB(UserActivityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
