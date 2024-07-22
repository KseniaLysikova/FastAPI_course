import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from models.user import User, Base


DATABASE_URL = "postgresql+asyncpg://sqlite:123456@localhost:5432/test"
engine = create_async_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


