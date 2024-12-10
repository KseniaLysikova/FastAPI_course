from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from schemas.enums import EnumRequestStatus
from crud.auth import get_user
from crud import get_user_info_by_id
from models.request import Request
from models.user import User, UserInfo
from core import errors
from schemas.supervisor import GetUserInfo
from schemas.project import ProjectStatisticsRequest, ProjectStatisticsResponse, WorkspaceStatisticsResponse


async def assign_request_to_attendant_crud(request_id: int, user_id: int, db: AsyncSession):
    user = get_user(db, user_id)
    if not user:
        raise errors.user_not_found()

    request = check_request_exists(request_id, db)
    request.attendant_id = user_id
    await db.commit()
    return


async def get_project_statistics_crud(project_id: int, filtration_params: ProjectStatisticsRequest, db: AsyncSession):
    query = select(Request).where(Request.project_id == project_id)

    if filtration_params.user_ids:
        query = query.where(Request.attendant_id.in_(filtration_params.user_ids))
    if filtration_params.from_date:
        query = query.where(Request.created_at >= filtration_params.from_date)
    if filtration_params.to_date:
        query = query.where(Request.created_at <= filtration_params.to_date)
    if filtration_params.position:
        query = query.where(UserInfo.position == filtration_params.position)

    total_requests = await db.execute(query.with_only_columns(func.count()))
    created_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.created).with_only_columns(
            func.count()
        )
    )
    in_work_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.in_work).with_only_columns(
            func.count()
        )
    )
    completed_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.completed).with_only_columns(
            func.count()
        )
    )
    closed_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.closed).with_only_columns(
            func.count()
        )
    )

    return ProjectStatisticsResponse(
        requests_all=total_requests.scalar(),
        requests_created=created_requests.scalar(),
        requests_in_work=in_work_requests.scalar(),
        requests_completed=completed_requests.scalar(),
        requests_closed=closed_requests.scalar(),
    )


async def get_workspace_overview_crud(filtration_params: WorkspaceStatisticsResponse, db: AsyncSession):
    query = select(Request).where(True)

    if filtration_params.project_ids:
        query = query.where(Request.project_id.in_(filtration_params.project_ids))
    if filtration_params.user_ids:
        query = query.where(Request.attendant_id.in_(filtration_params.user_ids))
    if filtration_params.from_date:
        query = query.where(Request.created_at >= filtration_params.from_date)
    if filtration_params.to_date:
        query = query.where(Request.created_at <= filtration_params.to_date)
    if filtration_params.position:
        query = query.where(UserInfo.position == filtration_params.position)

    total_requests = await db.execute(query.with_only_columns(func.count()))
    created_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.created).with_only_columns(
            func.count()
        )
    )
    in_work_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.in_work).with_only_columns(
            func.count()
        )
    )
    completed_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.completed).with_only_columns(
            func.count()
        )
    )
    closed_requests = await db.execute(
        query.where(Request.status == EnumRequestStatus.closed).with_only_columns(
            func.count()
        )
    )

    return ProjectStatisticsResponse(
        requests_all=total_requests.scalar(),
        requests_created=created_requests.scalar(),
        requests_in_work=in_work_requests.scalar(),
        requests_completed=completed_requests.scalar(),
        requests_closed=closed_requests.scalar(),
    )


async def get_user_details_crud(user_id: int, db: AsyncSession):
    user = await get_user(db, user_id)
    user_info = await get_user_info_by_id(db, user_id)
    '''if not user_info:
        raise errors.UserNotFound
    
    response = GetUserInfo(
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
    )

    return response'''
    return GetUserInfo(
        name="name",
        surname="surname",
        patronymic="test",
        username="username",
        email="test@gmail.com",
        phone="87986785",
        telegram_id=1,
        is_active=True,
        is_supervisor=False,
        position="position",
    )


async def check_request_exists(request_id: int, db: AsyncSession):
    request = await db.execute(select(Request).where(Request.id == request_id))
    request = request.scalars().first()
    if not request:
        raise errors.request_not_found
    return request
