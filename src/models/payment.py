from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func
import enum
from src.core.database import Base

class PaymentStatusEnum(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"

class PaymentMethodEnum(str, enum.Enum):
    selcom = "selcom"
    paypal = "paypal"
    stripe = "stripe"
    mpesa = "mpesa"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    order_id = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False, default="TZS")
    method = Column(SQLAlchemyEnum(PaymentMethodEnum), nullable=False)
    status = Column(SQLAlchemyEnum(PaymentStatusEnum), default=PaymentStatusEnum.pending, nullable=False)
    transaction_id = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
