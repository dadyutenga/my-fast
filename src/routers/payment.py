from fastapi import Depends, HTTPException, status, APIRouter
from src.middleware.auth import get_current_active_user
from src.models.user import User
from src.services.selcom_pay import selcom_pay
from src.schemas.payment import PaymentRequest, PaymentStatus

router = APIRouter()

@router.post("/payments/initiate")
async def initiate_payment(payment: PaymentRequest, current_user: User = Depends(get_current_active_user)):
    try:
        result = selcom_pay.create_order(
            amount=payment.amount,
            order_id=payment.order_id,
            buyer_email=payment.buyer_email,
            buyer_name=payment.buyer_name,
            buyer_phone=payment.buyer_phone
        )
        if result.get("result") == "SUCCESS":
            return {"message": "Payment initiated", "data": result.get("data")}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("message", "Payment initiation failed"))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/payments/status")
async def check_payment_status(status: PaymentStatus, current_user: User = Depends(get_current_active_user)):
    try:
        result = selcom_pay.check_order_status(status.order_id)
        if result.get("result") == "SUCCESS":
            return {"message": "Payment status retrieved", "data": result.get("data")}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result.get("message", "Payment status check failed"))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
