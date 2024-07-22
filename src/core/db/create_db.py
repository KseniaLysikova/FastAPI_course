import asyncio
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models.user import User, Base
from models.project import Project, ProjectUsers, DutySchedule
from models.request import Request, TelegramRequest


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


