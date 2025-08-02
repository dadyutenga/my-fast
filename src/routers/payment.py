from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.middleware.auth import get_current_active_user
from src.models.user import User
from src.models.payment import Payment, PaymentStatusEnum, PaymentMethodEnum
from src.services.selcom_pay import selcom_pay
from src.schemas.payment import PaymentRequest, PaymentInDB, PaymentUpdate

router = APIRouter()

@router.post("/payments", response_model=PaymentInDB)
async def create_payment(payment_request: PaymentRequest, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    # Create a new payment record in the database
    db_payment = Payment(
        user_id=current_user.id,
        order_id=payment_request.order_id,
        amount=payment_request.amount,
        currency=payment_request.currency,
        method=payment_request.method,
        status=PaymentStatusEnum.pending
    )
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)

    # Initiate payment with the respective gateway based on method
    if payment_request.method == PaymentMethodEnum.selcom:
        try:
            selcom_response = selcom_pay.create_order(
                amount=payment_request.amount,
                order_id=payment_request.order_id,
                buyer_email=payment_request.buyer_email,
                buyer_name=payment_request.buyer_name,
                buyer_phone=payment_request.buyer_phone
            )
            if selcom_response.get("result") == "SUCCESS":
                # Update payment status or transaction ID based on gateway response
                db_payment.status = PaymentStatusEnum.completed # This might be updated later via webhook
                db_payment.transaction_id = selcom_response.get("data", {}).get("trans_id")
                await db.commit()
                await db.refresh(db_payment)
                return db_payment
            else:
                db_payment.status = PaymentStatusEnum.failed
                await db.commit()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=selcom_response.get("message", "Selcom payment initiation failed")
                )
        except Exception as e:
            db_payment.status = PaymentStatusEnum.failed
            await db.commit()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Selcom payment error: {e}")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported payment method")

@router.get("/payments", response_model=list[PaymentInDB])
async def get_payments(skip: int = 0, limit: int = 100, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    payments = await db.query(Payment).filter(Payment.user_id == current_user.id).offset(skip).limit(limit).all()
    return payments

@router.get("/payments/{payment_id}", response_model=PaymentInDB)
async def get_payment_details(payment_id: int, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    payment = await db.query(Payment).filter(Payment.id == payment_id, Payment.user_id == current_user.id).first()
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    return payment

@router.put("/payments/{payment_id}", response_model=PaymentInDB)
async def update_payment_status(payment_id: int, payment_update: PaymentUpdate, db: AsyncSession = Depends(get_db), _ = Depends(role_required([Role.admin, Role.superadmin]))):
    db_payment = await db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    for key, value in payment_update.dict(exclude_unset=True).items():
        setattr(db_payment, key, value)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment
