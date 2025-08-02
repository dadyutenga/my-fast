from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import role_required, get_current_active_user
from src.models.user import Role, User
from src.models.user_activity import UserActivity
from src.schemas.user_activity import UserActivityCreate, UserActivityInDB

router = APIRouter()

@router.post("/activities", response_model=UserActivityInDB)
async def log_user_activity(activity: UserActivityCreate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_activity = UserActivity(**activity.dict())
    db.add(db_activity)
    await db.commit()
    await db.refresh(db_activity)
    return db_activity

@router.get("/activities", response_model=list[UserActivityInDB])
async def get_user_activities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    activities = await db.query(UserActivity).offset(skip).limit(limit).all()
    return activities

@router.get("/my-activities", response_model=list[UserActivityInDB])
async def get_my_activities(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    activities = await db.query(UserActivity).filter(UserActivity.user_id == current_user.id).offset(skip).limit(limit).all()
    return activities
