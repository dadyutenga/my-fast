from fastapi import Depends, APIRouter, HTTPException, status
from src.middleware.auth import role_required
from src.models.user import Role
import json

router = APIRouter()

# Dummy storage for metrics (replace with proper storage in production)
metrics_data = {
    "request_count": 0,
    "endpoint_stats": {},
    "error_count": 0
}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.get("/metrics")
async def get_metrics(_ = Depends(role_required([Role.admin, Role.superadmin]))):
    return metrics_data
