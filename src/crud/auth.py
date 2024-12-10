from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from passlib.context import CryptContext
import string
import random


pwd_context = CryptContext(schemes=["bcrypt"])


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await db.execute(select(User).where(User.username == username))
    user = user.scalars().first()
    if user and pwd_context.verify(password, user.password):
        return user
    return None


def generate_password(length: int = 12):
    characters = string.ascii_letters + string.digits + string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))

    return password
