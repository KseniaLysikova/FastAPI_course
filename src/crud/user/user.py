from fastapi import Request
from typing import Optional
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core import errors
from models.user import User
from core.auth import verify_user_access
from crud import get_user_info_by_id
from crud.auth import get_user
from schemas.user import PasswordUpdate, GetMyInfo, GetMyStatistics, UpdateUserInfo
from schemas.enums import EnumRequestStatus


async def get_my_info_crud(request: Request, db: AsyncSession):
    access_token = request.cookies.get("Authorization")
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    if not access_token:
        raise errors.unauthorized()

    user = await verify_user_access(access_token, db)
    if not user:
        raise errors.unauthorized()

    user_info = await get_user_info_by_id(db, user.id)
    if not user_info:
        raise errors.user_not_found()

    return GetMyInfo(
        name=user_info.name,
        surname=user_info.surname,
        patronymic=user_info.patronymic,
        username=user.username,
        email=user.email,
        phone=user_info.phone,
        telegram_id=user.telegram_id,
        is_active=user.is_active,
        is_supervisor=user.is_supervisor,
        position=user_info.position,
        token=access_token,
    )


async def get_my_statistics_crud(current_user: User, db: AsyncSession):
    query = select(Request).where(True)
    if current_user.id:
        query = query.where(Request.attendant_id == current_user.id)

        total_requests = await db.execute(query.with_only_columns(func.count()))
        in_work_requests = await db.execute(
            query.where(Request.status == EnumRequestStatus.in_work).with_only_columns(
                func.count()
            )
        )
        completed_requests = await db.execute(
            query.where(
                Request.status == EnumRequestStatus.completed
            ).with_only_columns(func.count())
        )
        closed_requests = await db.execute(
            query.where(Request.status == EnumRequestStatus.closed).with_only_columns(
                func.count()
            )
        )

        return GetMyStatistics(
            requests_total=total_requests.scalar(),
            requests_in_work=in_work_requests.scalar(),
            requests_completed=completed_requests.scalar(),
            requests_closed=closed_requests.scalar(),
            average_close_time_in_seconds=0,
            average_pick_up_time_in_seconds=0,
        )
    raise errors.UserNotFound()


async def update_account_info_crud(update_data: UpdateUserInfo, user_id: int, db: AsyncSession,):
    user = await get_user(db, user_id)
    user_info = await get_user_info_by_id(db, user_id)
    if (not user) or (not user_info):
        raise errors.user_not_found

    if update_data.email is not None:
        if "@" not in update_data.email:
            raise errors.email_format_error()

    if update_data.name is not None:
        user_info.name = update_data.name
    if update_data.surname is not None:
        user_info.surname = update_data.surname
    if update_data.patronymic is not None:
        user_info.patronymic = update_data.patronymic
    if update_data.phone is not None:
        user_info.phone = update_data.phone
    if update_data.email is not None:
        user.email = update_data.email
    if update_data.telegram_id is not None:
        user.telegram_id = update_data.telegram_id
    if update_data.is_supervisor is not None:
        user.is_supervisor = update_data.is_supervisor
    if update_data.position is not None:
        user_info.position = update_data.position
    await db.commit()
