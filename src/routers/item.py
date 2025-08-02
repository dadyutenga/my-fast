from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.models.item import Item
from src.schemas.item import ItemCreate, ItemUpdate, ItemInDB
from src.middleware.auth import role_required
from src.models.user import Role

router = APIRouter()

@router.post("/items", response_model=ItemInDB)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.post("/items/bulk", response_model=list[ItemInDB])
async def create_items_bulk(items: list[ItemCreate], db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_items = [Item(**item.dict()) for item in items]
    db.bulk_save_objects(db_items)
    await db.commit()
    return db_items

@router.get("/items", response_model=list[ItemInDB])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    items = await db.query(Item).offset(skip).limit(limit).all()
    return items

@router.get("/items/{item_id}", response_model=ItemInDB)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: int, item_update: ItemUpdate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_item = await db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    for key, value in item_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}", response_model=ItemInDB)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_item = await db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    await db.delete(db_item)
    await db.commit()
    return db_item
