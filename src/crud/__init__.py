from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User, UserInfo
from core import errors


async def get_user_info_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(UserInfo).where(UserInfo.user_id == user_id)
    )
    user = result.scalars().first()
    return user
