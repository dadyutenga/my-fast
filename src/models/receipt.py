from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.core.database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, index=True)
    items = Column(String, nullable=False)  # JSON string of items
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
