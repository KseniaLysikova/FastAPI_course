from fastapi import APIRouter
from routers.v1.project.project import router as project
from routers.v1.user.user import router as user
from routers.v1.user.request import router as user_request
from routers.v1.auth.auth import router as auth
from routers.v1.supervisor.supervisor import router as supervisor_request
from routers.v1.supervisor.admin import router as supervisor_admin
from routers.v1.supervisor.project import router as supervisor_project


router = APIRouter(prefix="/v1")
router.include_router(auth, prefix="/user", tags=["Auth"])
router.include_router(project, prefix="/project", tags=["Project"])
router.include_router(user, prefix="/user", tags=["User"])
router.include_router(user_request, prefix="/request", tags=["User"])
router.include_router(supervisor_request, prefix="/request", tags=["Supervisor"])
router.include_router(supervisor_admin, prefix="/user", tags=["Supervisor"])
router.include_router(supervisor_project, prefix="/project", tags=["Supervisor"])