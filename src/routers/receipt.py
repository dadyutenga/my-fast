from fastapi import Depends, HTTPException, status, APIRouter
import json
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import role_required
from src.models.user import Role
from src.models.receipt import Receipt
from src.schemas.receipt import ReceiptCreate, ReceiptInDB

router = APIRouter()

@router.post("/receipts", response_model=ReceiptInDB)
async def create_receipt(receipt: ReceiptCreate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    items_json = json.dumps(receipt.items)
    db_receipt = Receipt(order_id=receipt.order_id, items=items_json, total=receipt.total)
    db.add(db_receipt)
    await db.commit()
    await db.refresh(db_receipt)
    db_receipt.items = json.loads(db_receipt.items)
    return db_receipt

@router.get("/receipts/{receipt_id}", response_model=ReceiptInDB)
async def get_receipt(receipt_id: int, db: AsyncSession = Depends(get_db)):
    receipt = await db.query(Receipt).filter(Receipt.id == receipt_id).first()
    if receipt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receipt not found")
    receipt.items = json.loads(receipt.items)
    return receipt

@router.get("/receipts", response_model=list[ReceiptInDB])
async def get_receipts(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    receipts = await db.query(Receipt).offset(skip).limit(limit).all()
    for receipt in receipts:
        receipt.items = json.loads(receipt.items)
    return receipts
