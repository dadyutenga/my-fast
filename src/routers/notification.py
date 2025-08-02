from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import role_required, get_current_active_user
from src.models.user import Role, User
from src.models.notification import Notification
from src.schemas.notification import NotificationCreate, NotificationUpdate, NotificationInDB
from src.services.email import send_email

router = APIRouter()

@router.post("/notifications", response_model=NotificationInDB)
async def create_notification(notification: NotificationCreate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    user = await db.query(User).filter(User.id == notification.user_id).first()
    if user:
        await send_email(user.email, notification.title, notification.message)
    return db_notification

@router.get("/notifications", response_model=list[NotificationInDB])
async def get_notifications(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    notifications = await db.query(Notification).offset(skip).limit(limit).all()
    return notifications

@router.get("/my-notifications", response_model=list[NotificationInDB])
async def get_my_notifications(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    notifications = await db.query(Notification).filter(Notification.user_id == current_user.id).offset(skip).limit(limit).all()
    return notifications

@router.put("/notifications/{notification_id}", response_model=NotificationInDB)
async def update_notification(notification_id: int, update: NotificationUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_notification = await db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == current_user.id).first()
    if db_notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found or access denied")
    db_notification.is_read = update.is_read
    await db.commit()
    await db.refresh(db_notification)
    return db_notification
