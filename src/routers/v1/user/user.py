from fastapi import APIRouter, Depends, Request
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.create_db import get_async_database
from core import errors
from schemas.user import PasswordUpdate, GetMyInfo, GetMyStatistics, UpdateUserInfo
from models.user import User
from core.auth import verify_user_access, get_current_user
from crud.user.user import (
    get_my_info_crud,
    get_my_statistics_crud,
    update_account_info_crud
)

router = APIRouter()


@router.get('/me',
            response_model=GetMyInfo,
            responses=errors.with_errors())
async def get_my_info(request: Request, db: AsyncSession = Depends(get_async_database)):
    info = await get_my_info_crud(request, db)
    return info


@router.put("/me/password",
            status_code=204,
            responses=errors.with_errors())
async def change_my_password(
        update_data: PasswordUpdate,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_database)
):
    if not current_user.verify_password(update_data.old_password):
        raise errors.incorrect_password()
    current_user.password = update_data.new_password

    db.add(current_user)
    await db.commit()

    return


@router.get('/me/statistics',
            response_model=GetMyStatistics,
            responses=errors.with_errors())
async def get_my_statistics(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_database)
):
    stats = await get_my_statistics_crud(current_user, db)
    return


@router.put('/info',
            status_code=204,
            responses=errors.with_errors())
async def update_account_info(update_data: UpdateUserInfo,
                              user_id: int,
                              db: AsyncSession = Depends(get_async_database)):
    await update_account_info_crud(update_data, user_id, db)
    return
