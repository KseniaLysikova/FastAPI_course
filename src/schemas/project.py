from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.enums import EnumRequestStatus, EnumOrderByType


class ProjectCreate(BaseModel):
    name: str
    bot_id: int
    description: Optional[str]
    help_information: Optional[str]


class ProjectGet(BaseModel):
    name: str
    description: Optional[str]
    help_information: Optional[str]
    default_attendant_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]


class ProjectBaseInfo(BaseModel):
    id: int
    name: str
    created_at: datetime


class ProjectGetAll(BaseModel):
    projects: List[ProjectBaseInfo]


class ProjectUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    help_information: Optional[str]
    default_attendant_id: Optional[int]


class ProjectUser(BaseModel):
    id: int
    fullname: str
    position: str
    is_supervisor: bool
    is_active: bool


class ProjectRequestBaseInfo(BaseModel):
    request_id: int
    status: EnumRequestStatus
    attendant_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]


class ProjectStatisticsRequest(BaseModel):
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    position: Optional[str]
    user_ids: Optional[List[int]]


class WorkspaceStatisticsResponse(BaseModel):
    project_ids: Optional[List[int]]
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    position: Optional[str]
    user_ids: Optional[List[int]]


class ProjectStatisticsResponse(BaseModel):
    requests_all: int
    requests_created: int
    requests_in_work: int
    requests_completed: int
    requests_closed: int