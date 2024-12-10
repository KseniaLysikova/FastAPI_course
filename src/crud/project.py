from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.project import Project, ProjectUsers
from models.user import User
from schemas.project import ProjectCreate, ProjectUpdate, ProjectUser
from core.errors import project_not_found


async def create_project_crud(project_info: ProjectCreate, db: AsyncSession):
    new_project = Project(
        name=project_info.name,
        description=project_info.description,
        help_information=project_info.help_information,
        bot_id=project_info.bot_id,
        default_attendant_id=None
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


async def get_project_by_id_crud(project_id: int, db: AsyncSession):
    project = await db.execute((select(Project).where(Project.id == project_id)))
    return project.scalars().first()


async def get_all_projects_crud(db: AsyncSession):
    projects = await db.execute(select(Project))
    return projects.scalars().all()


async def delete_project_crud(project_id: int, db: AsyncSession):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    if project:
        await db.delete(project)
        await db.commit()
    else:
        raise project_not_found


async def update_project_crud(project_id: int, project_info: ProjectUpdate, db: AsyncSession):
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalars().first()
    if not project:
        raise project_not_found

    if project_info.name is not None:
        project.name = project_info.name
    if project_info.description is not None:
        project.description = project_info.description
    if project_info.help_information is not None:
        project.help_information = project_info.help_information
    if project_info.default_attendant_id is not None:
        project.default_attendant_id = project_info.default_attendant_id

    await db.commit()
    await db.refresh(project)
    return project


async def get_all_project_users_crud(project_id: int, db: AsyncSession):
    result = await db.execute(
        select(ProjectUsers)
        .where(ProjectUsers.project_id == project_id)
    )
    project_users = result.scalars().all()
    user_details = []
    print(project_users)
    for project_user in project_users:
        user_result = await db.execute(
            select(User).where(User.id == project_user.user_id)
        )
        user = user_result.scalars().first()

        if user:
            user_details.append({
                "id": user.id,
                "fullname": f"{user.username}",
                "position": user.position if hasattr(user, "position") else "Unknown",
                "is_supervisor": project_user.is_on_duty,
                "is_active": user.is_active
            })
    return user_details
