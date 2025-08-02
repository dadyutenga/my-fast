from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MediaBase(BaseModel):
    filename: str
    content_type: str

class MediaCreate(MediaBase):
    filepath: str

class MediaInDB(MediaBase):
    id: int
    filepath: str
    created_at: datetime

    class Config:
        orm_mode = True
