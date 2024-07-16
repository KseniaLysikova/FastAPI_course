import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase


pg_url = "postgresql+asyncpg://postgres:123456@localhost:5432/"
engine = create_async_engine(pg_url, echo=True)
session = AsyncSession(engine)


class Base(DeclarativeBase):
    pass


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()

asyncio.run(create_db())
