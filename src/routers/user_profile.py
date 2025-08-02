from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import get_current_active_user
from src.models.user import User
from src.schemas.user import UserUpdate, UserInDB
from src.utils.password import get_password_hash

router = APIRouter()

@router.put("/me", response_model=UserInDB)
async def update_user_profile(user_update: UserUpdate, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    if user_update.email and user_update.email != current_user.email:
        existing_user = await db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        current_user.email = user_update.email
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    if user_update.role:
        current_user.role = user_update.role
    await db.commit()
    await db.refresh(current_user)
    return current_user
