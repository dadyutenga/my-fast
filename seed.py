import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import async_session, engine, Base
from src.models.user import User, Role
from src.utils.password import get_password_hash

async def seed_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:  # type: AsyncSession
        # Create a default admin user if not exists
        admin_user = await session.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            hashed_password = get_password_hash("adminpassword")
            admin_user = User(email="admin@example.com", hashed_password=hashed_password, role=Role.admin)
            session.add(admin_user)
            await session.commit()
            print("Default admin user created: admin@example.com / adminpassword")
        else:
            print("Default admin user already exists.")

if __name__ == "__main__":
    asyncio.run(seed_database())
