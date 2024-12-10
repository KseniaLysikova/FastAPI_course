from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import datetime
from core import errors
from core.db.create_db import get_async_database
from crud.project import (
    create_project_crud,
    get_project_by_id_crud,
    get_all_projects_crud,
    delete_project_crud,
    update_project_crud,
    get_all_project_users_crud
)
from schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectGet,
    ProjectGetAll,
    ProjectBaseInfo,
    ProjectUser
)

router = APIRouter()


@router.post("",
             status_code=201,
             responses=errors.with_errors())
async def create_project(project_info: ProjectCreate, db: AsyncSession = Depends(get_async_database)):
    new_project = await create_project_crud(project_info, db)
    return new_project


@router.get("/{project_id}/",
            response_model=ProjectGet,
            responses=errors.with_errors())
async def get_project_by_id(project_id: int, db: AsyncSession = Depends(get_async_database)):
    project = await get_project_by_id_crud(project_id, db)
    if not project:
        raise errors.project_not_found
    return ProjectGet(name=project.name,
                      description=project.description,
                      help_information=project.help_information,
                      default_attendant_id=1,
                      created_at=datetime.now(),
                      updated_at=datetime.now())


@router.get("/all",
            response_model=ProjectGetAll,
            responses=errors.with_errors())
async def get_all_projects(db: AsyncSession = Depends(get_async_database)):
    projects = await get_all_projects_crud(db)
    return ProjectGetAll(
        projects=[
            ProjectBaseInfo(id=project.id, name=project.name, created_at=project.created_at)
            for project in projects
        ]
    )


@router.delete("/{project_id}",
               status_code=204,
               responses=errors.with_errors())
async def delete_project(project_id: int, db: AsyncSession = Depends(get_async_database)):
    await delete_project_crud(project_id, db)
    return {"status": "success"}


@router.patch("/{project_id}",
              status_code=204,
              responses=errors.with_errors())
async def update_project(project_id: int, project_info: ProjectUpdate, db: AsyncSession = Depends(get_async_database)):
    updated_project = await update_project_crud(project_id, project_info, db)
    return {"status": "success"}


@router.get("/{project_id}/users",
            response_model=List[ProjectUser],
            responses=errors.with_errors())
async def get_all_project_users(project_id: int, db: AsyncSession = Depends(get_async_database)):
    users = await get_all_project_users_crud(project_id, db)
    return [
        ProjectUser(
            id=user['id'],
            fullname=user['fullname'],
            position=user['position'],
            is_supervisor=user['is_supervisor'],
            is_active=user['is_active']
        ) for user in users
    ]
