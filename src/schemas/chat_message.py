from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    receiver_id: int
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageUpdate(BaseModel):
    is_read: bool

class ChatMessageInDB(ChatMessageBase):
    id: int
    sender_id: int
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
