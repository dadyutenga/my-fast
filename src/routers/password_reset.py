from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import random
import string

from src.core.database import get_db
from src.services.email import send_email
from src.models.user import User
from src.utils.password import get_password_hash
import redis
from src.config.settings import settings

router = APIRouter()

r = redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)

def generate_reset_code(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for i in range(length))

@router.post("/password-reset/request")
async def request_password_reset(email: str, db: AsyncSession = Depends(get_db)):
    user = await db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    reset_code = generate_reset_code()
    r.setex(f"reset:{email}", 3600, reset_code)  # Expires in 1 hour
    await send_email(email, "Password Reset", f"Your password reset code is {reset_code}")
    return {"message": "Password reset code sent to email"}

@router.post("/password-reset/confirm")
async def confirm_password_reset(email: str, code: str, new_password: str, db: AsyncSession = Depends(get_db)):
    stored_code = r.get(f"reset:{email}")
    if stored_code is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset code expired or not found")
    if stored_code != code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset code")
    user = await db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")
    user.hashed_password = get_password_hash(new_password)
    await db.commit()
    r.delete(f"reset:{email}")
    return {"message": "Password reset successful"}
