from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db.create_db import get_async_database
from crud.supervisor.supervisor import (
    assign_request_to_attendant_crud,
    get_project_statistics_crud,
    get_workspace_overview_crud,
    get_user_details_crud
)
from core import errors
from schemas.supervisor import GetUserInfo
from schemas.project import ProjectStatisticsRequest, ProjectStatisticsResponse, WorkspaceStatisticsResponse

router = APIRouter()


@router.post("/{request_id}/assign",
             status_code=204,
             responses=errors.with_errors())
async def assign_request_to_attendant(request_id: int, user_id: int,
                                      db: AsyncSession = Depends(get_async_database)):
    await assign_request_to_attendant_crud(request_id, user_id, db)
    return


@router.post("/overview/project/{project_id}",
             response_model=ProjectStatisticsResponse,
             responses=errors.with_errors())
async def get_project_statistics(project_id: int,
                                 filtration_params: ProjectStatisticsRequest,
                                 db: AsyncSession = Depends(get_async_database)):
    stats = await get_project_statistics_crud(project_id, filtration_params, db)
    return stats


@router.post("/overview/all",
             response_model=ProjectStatisticsResponse,
             responses=errors.with_errors())
async def get_workspace_overview(filtration_params: WorkspaceStatisticsResponse,
                                 db: AsyncSession = Depends(get_async_database)):
    workspace_stats = await get_workspace_overview_crud(filtration_params, db)
    return workspace_stats


@router.get("/{user_id}",
            response_model=GetUserInfo,
            responses=errors.with_errors())
async def get_user_details(user_id: int):
    return GetUserInfo(
        name="name",
        surname="surname",
        patronymic="test",
        username="username",
        email="test@gmail.com",
        phone="87986785",
        telegram_id="1",
        is_active=True,
        is_supervisor=False,
        position="position",
    )
