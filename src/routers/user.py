from fastapi import Depends, APIRouter
from src.middleware.auth import get_current_active_user
from src.models.user import User
from src.schemas.user import UserInDB

router = APIRouter()

@router.get("/me", response_model=UserInDB)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
