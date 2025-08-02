from fastapi import FastAPI
from src.routers import auth, user, admin, otp, metrics, payment, receipt, media, password_reset, item, user_profile, user_activity, notification, audit_log
from src.core.database import engine, Base
from src.middleware.metrics import MetricsMiddleware
from src.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(title="FastAPI Backend", description="A scalable FastAPI backend with authentication and more.")

app.add_middleware(MetricsMiddleware)
app.add_middleware(RateLimitMiddleware, rate_limit=100, per_seconds=60)

# Create database tables
@app.on_event("startup")
async def startup_db_client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(user.router, prefix="/api", tags=["user"])
app.include_router(admin.router, prefix="/api", tags=["admin"])
app.include_router(otp.router, prefix="/api", tags=["otp"])
app.include_router(metrics.router, prefix="/api", tags=["metrics"])
app.include_router(payment.router, prefix="/api", tags=["payment"])
app.include_router(receipt.router, prefix="/api", tags=["receipt"])
app.include_router(media.router, prefix="/api", tags=["media"])
app.include_router(password_reset.router, prefix="/api", tags=["password_reset"])
app.include_router(item.router, prefix="/api", tags=["item"])
app.include_router(user_profile.router, prefix="/api", tags=["user_profile"])
app.include_router(user_activity.router, prefix="/api", tags=["user_activity"])
app.include_router(notification.router, prefix="/api", tags=["notification"])
app.include_router(audit_log.router, prefix="/api", tags=["audit_log"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend"}
