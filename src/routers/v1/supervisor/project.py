from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.create_db import get_async_database
from crud.supervisor.project import add_attendant_to_project_crud, remove_attendant_from_project_crud
from core import errors

router = APIRouter()


@router.post("/{project_id}/attendant",
             status_code=204,
             responses=errors.with_errors())
async def add_attendant_to_project(project_id: int, user_id: int, db: AsyncSession = Depends(get_async_database)):
    await add_attendant_to_project_crud(project_id, user_id, db)
    return


@router.delete("/{project_id}/attendant",
               status_code=204,
               responses=errors.with_errors())
async def remove_attendant_from_project(project_id: int, user_id: int, db: AsyncSession = Depends(get_async_database)):
    await remove_attendant_from_project_crud(project_id, user_id, db)
    return
