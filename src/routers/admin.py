from fastapi import Depends, APIRouter, HTTPException, status
from src.middleware.auth import role_required
from src.models.user import User, Role
from src.schemas.user import UserInDB
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db

router = APIRouter()

@router.get("/users", response_model=list[UserInDB])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    users = await db.query(User).offset(skip).limit(limit).all()
    return users
