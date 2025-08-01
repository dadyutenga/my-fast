from fastapi import FastAPI
from src.routers import auth, user, admin, otp, metrics
from src.core.database import engine, Base

app = FastAPI(title="FastAPI Backend", description="A scalable FastAPI backend with authentication and more.")

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

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Backend"}
