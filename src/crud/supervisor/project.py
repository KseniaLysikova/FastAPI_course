from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from crud.auth import get_user
from models.project import Project
from models.project import ProjectUsers
from sqlalchemy.exc import IntegrityError
from core import errors


async def add_attendant_to_project_crud(project_id: int, user_id: int, db: AsyncSession):
    await check_project_exists(project_id, db)
    await check_user_exists(user_id, db)

    await check_user_not_in_project(project_id, user_id, db)

    new_attendant = ProjectUsers(project_id=project_id, user_id=user_id, is_on_duty=True)

    db.add(new_attendant)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise errors.invalid_project_user_id()

    return new_attendant


async def remove_attendant_from_project_crud(project_id: int, user_id: int, db: AsyncSession):
    await check_project_exists(project_id, db)
    await check_user_exists(user_id, db)

    user = await check_user_in_project(project_id, user_id, db)

    await db.delete(user)
    await db.commit()
    return


async def check_user_exists(user_id: int, db: AsyncSession):
    user = get_user(db, user_id)
    if not user:
        raise errors.user_not_found()
    return user


async def check_project_exists(project_id: int, db: AsyncSession):
    project_check = await db.execute(select(Project).where(
        Project.id == project_id
    ))
    project = project_check.scalars().first()
    if not project:
        raise errors.project_not_found()
    return project


async def check_user_not_in_project(project_id: int, user_id: int, db: AsyncSession):
    result = await db.execute(select(ProjectUsers).where(
        ProjectUsers.project_id == project_id,
        ProjectUsers.user_id == user_id
        )
    )
    project_user = result.scalars().first()
    if project_user is not None:
        raise errors.project_user_exists()
    return project_user


async def check_user_in_project(project_id: int, user_id: int, db: AsyncSession):
    project_user_check = await db.execute(select(ProjectUsers).where(
        ProjectUsers.project_id == project_id,
        ProjectUsers.user_id == user_id
    ))
    project_user = project_user_check.scalars().first()
    if not project_user:
        raise errors.user_not_in_project()
    return project_user
