from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import get_current_active_user
from src.models.user import User
from src.models.chat_message import ChatMessage
from src.schemas.chat_message import ChatMessageCreate, ChatMessageUpdate, ChatMessageInDB

router = APIRouter()

@router.post("/messages", response_model=ChatMessageInDB)
async def send_message(message: ChatMessageCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_message = ChatMessage(sender_id=current_user.id, **message.dict())
    db.add(db_message)
    await db.commit()
    await db.refresh(db_message)
    return db_message

@router.get("/messages/sent", response_model=list[ChatMessageInDB])
async def get_sent_messages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    messages = await db.query(ChatMessage).filter(ChatMessage.sender_id == current_user.id).offset(skip).limit(limit).all()
    return messages

@router.get("/messages/received", response_model=list[ChatMessageInDB])
async def get_received_messages(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    messages = await db.query(ChatMessage).filter(ChatMessage.receiver_id == current_user.id).offset(skip).limit(limit).all()
    return messages

@router.put("/messages/{message_id}", response_model=ChatMessageInDB)
async def update_message(message_id: int, update: ChatMessageUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_message = await db.query(ChatMessage).filter(ChatMessage.id == message_id, ChatMessage.receiver_id == current_user.id).first()
    if db_message is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found or access denied")
    db_message.is_read = update.is_read
    await db.commit()
    await db.refresh(db_message)
    return db_message
