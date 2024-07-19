import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "postgresql+asyncpg://postgres:123456@localhost:5432/"
engine = create_async_engine(DATABASE_URL, echo=True)
session = AsyncSession(engine)


Base = DeclarativeBase


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
