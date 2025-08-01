from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import random
import string

from src.core.database import get_db
from src.services.email import send_email
from src.services.sms import send_sms
from src.config.settings import settings
import redis

router = APIRouter()

r = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

def generate_otp(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))

@router.post("/send-email-otp")
async def send_email_otp(email: str, db: AsyncSession = Depends(get_db)):
    otp = generate_otp()
    r.setex(f"otp:email:{email}", 300, otp)  # Expires in 5 minutes
    await send_email(email, "Your OTP Code", f"Your OTP code is {otp}")
    return {"message": "OTP sent to email"}

@router.post("/send-sms-otp")
async def send_sms_otp(phone: str, db: AsyncSession = Depends(get_db)):
    otp = generate_otp()
    r.setex(f"otp:sms:{phone}", 300, otp)  # Expires in 5 minutes
    await send_sms(phone, f"Your OTP code is {otp}")
    return {"message": "OTP sent to SMS"}

@router.post("/verify-otp")
async def verify_otp(email_or_phone: str, otp: str, db: AsyncSession = Depends(get_db)):
    key = f"otp:email:{email_or_phone}" if "@" in email_or_phone else f"otp:sms:{email_or_phone}"
    stored_otp = r.get(key)
    if stored_otp is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP expired or not found")
    if stored_otp != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    r.delete(key)
    return {"message": "OTP verified"}
