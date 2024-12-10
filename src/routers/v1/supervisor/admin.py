from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.create_db import get_async_database
from crud.supervisor.admin import (
    sing_up_user_crud,
    delete_user_crud,
    user_status_update_crud,
    supervisor_status_update_crud
)
from core import errors
from schemas.supervisor import UserSignUp

router = APIRouter()


@router.post("/sign_up",
             status_code=202,
             responses=errors.with_errors())
async def sign_up_user(signup_data: UserSignUp, db: AsyncSession = Depends(get_async_database)):
    new_user = await sing_up_user_crud(signup_data, db)
    return


@router.delete("/{user_id}",
               status_code=204,
               responses=errors.with_errors())
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_database)):
    await delete_user_crud(user_id, db)
    return


@router.put("/activation_status/update",
            status_code=204,
            responses=errors.with_errors())
async def user_status_update(user_id: int, is_active: bool, db: AsyncSession = Depends(get_async_database)):
    await user_status_update_crud(user_id, is_active, db)
    return


@router.put("/supervisor_status/update",
            status_code=204,
            responses=errors.with_errors())
async def supervisor_status_update(user_id: int, is_supervisor: bool, db: AsyncSession = Depends(get_async_database)):
    await supervisor_status_update_crud(user_id, is_supervisor, db)
    return
