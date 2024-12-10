from fastapi import APIRouter
from typing import List

from core import errors
from schemas.user import RequestResponse, ProjectRequestBaseInfo, RequestsAllProjectRequest, CreateTelegramRequest
from schemas.enums import EnumRequestStatus


router = APIRouter()


@router.post("/{project_id}/requests/all",
             response_model=List[ProjectRequestBaseInfo],
             responses=errors.with_errors())
async def get_all_project_requests(filtration_params: RequestsAllProjectRequest):
    pass


@router.post("/{project_id}/create",
             status_code=201,
             responses=errors.with_errors())
async def create_request(project_id: int, params: CreateTelegramRequest):
    """Temporally endpoint for testing. Delete this before release!"""
    pass


@router.get("/{request_id}",
            response_model=RequestResponse,
            responses=errors.with_errors())
async def get_request_by_id(request_id: int):
    """Get information about a specific request"""
    pass


@router.put('/{request_id}/status',
            status_code=204,
            responses=errors.with_errors())
async def update_request_status(request_id: int, status: EnumRequestStatus):
    """Set new status of a specific request"""
    pass