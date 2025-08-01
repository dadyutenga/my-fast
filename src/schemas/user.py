from pydantic import BaseModel, EmailStr, Field
from typing import Optional

from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    superadmin = "superadmin"

class UserBase(BaseModel):
    email: EmailStr
    role: Role = Role.user

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
