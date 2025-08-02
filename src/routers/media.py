from fastapi import Depends, HTTPException, status, APIRouter, UploadFile, File
import os
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import role_required
from src.models.user import Role
from src.models.media import Media
from src.schemas.media import MediaInDB

router = APIRouter()

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/media", response_model=MediaInDB)
async def upload_media(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    db_media = Media(filename=file.filename, filepath=filepath, content_type=file.content_type)
    db.add(db_media)
    await db.commit()
    await db.refresh(db_media)
    return db_media

@router.get("/media/{media_id}", response_model=MediaInDB)
async def get_media(media_id: int, db: AsyncSession = Depends(get_db)):
    media = await db.query(Media).filter(Media.id == media_id).first()
    if media is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Media not found")
    return media
