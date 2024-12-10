from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from crud.auth import get_user, generate_password
from models.user import User, UserInfo
from schemas.supervisor import UserSignUp
from sqlalchemy.exc import IntegrityError
from core import errors


async def sing_up_user_crud(signup_data: UserSignUp, db: AsyncSession):
    if "@" not in signup_data.email:
        raise errors.email_format_error()
    user = await check_username_email_exists(signup_data, db)
    if user:
        raise errors.user_already_exists

    password = generate_password()
    new_user = User(
        username=signup_data.username,
        email=signup_data.email,
        password=password,
        telegram_id=None,
        is_active=True,
    )

    db.add(new_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise IntegrityError

    user_info = UserInfo(
        user_id=new_user.id,
        surname=signup_data.surname,
        name=signup_data.name,
        patronymic=signup_data.patronymic,
        phone=None,
        position=signup_data.position,
    )

    db.add(user_info)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise IntegrityError

    return new_user


async def delete_user_crud(user_id: int, db: AsyncSession):
    user = await get_user(db, user_id)
    if not user:
        raise errors.user_not_found()
    await db.delete(user)
    await db.commit()
    return


async def user_status_update_crud(user_id: int, is_active: bool, db: AsyncSession):
    user = await get_user(db, user_id)
    if not user:
        raise errors.user_not_found()
    user.is_active = is_active
    await db.commit()
    return user


async def supervisor_status_update_crud(user_id: int, is_supervisor: bool, db: AsyncSession):
    user = await get_user(db, user_id)
    if not user:
        raise errors.user_not_found()
    user.is_supervisor = is_supervisor
    await db.commit()
    return user


async def check_username_email_exists(signup_data: UserSignUp, db: AsyncSession):
    result = await db.execute(select(User).where(
        User.email == signup_data.email,
        User.username == signup_data.username
    ))
    user = result.scalars().first()
    return user
