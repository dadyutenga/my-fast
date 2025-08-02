from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import role_required, get_current_active_user
from src.models.user import Role, User
from src.models.audit_log import AuditLog
from src.schemas.audit_log import AuditLogCreate, AuditLogInDB

router = APIRouter()

@router.post("/audit-logs", response_model=AuditLogInDB)
async def log_audit(audit: AuditLogCreate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_audit = AuditLog(**audit.dict())
    db.add(db_audit)
    await db.commit()
    await db.refresh(db_audit)
    return db_audit

@router.get("/audit-logs", response_model=list[AuditLogInDB])
async def get_audit_logs(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    logs = await db.query(AuditLog).offset(skip).limit(limit).all()
    return logs

@router.get("/audit-logs/entity/{entity_type}/{entity_id}", response_model=list[AuditLogInDB])
async def get_entity_audit_logs(entity_type: str, entity_id: int, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    logs = await db.query(AuditLog).filter(AuditLog.entity_type == entity_type, AuditLog.entity_id == entity_id).offset(skip).limit(limit).all()
    return logs
