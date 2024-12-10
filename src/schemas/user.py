from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

from schemas.enums import EnumRequestStatus, EnumOrderByType


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class GetMyInfo(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str]
    username: str
    email: EmailStr
    phone: Optional[str]
    telegram_id: Optional[str]
    is_active: bool
    is_supervisor: bool
    position: str
    token: str


class GetMyStatistics(BaseModel):
    requests_total: int
    requests_in_work: int
    requests_closed: int
    requests_completed: int
    average_close_time_in_seconds: int
    average_pick_up_time_in_seconds: int


class UpdateUserInfo(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    telegram_id: Optional[str]
    is_supervisor: Optional[bool]
    position: Optional[str]


class RequestLogMessage(BaseModel):
    message_id: int
    user_id: int
    message_content: str
    created_at: datetime


class RequestResponse(BaseModel):
    status: EnumRequestStatus
    request_message: List[RequestLogMessage]


class ProjectRequestBaseInfo(BaseModel):
    request_id: int
    status: EnumRequestStatus
    attendant_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]


class RequestsAllProjectRequest(BaseModel):
    project_id: Optional[int]
    user_id: Optional[int]
    limit: int = 20,
    offset: int = 0
    from_date: Optional[datetime]
    to_date: Optional[datetime]
    user_position: Optional[str]
    status: Optional[EnumRequestStatus]
    order_by_creation: EnumOrderByType = EnumOrderByType.descending


class CreateTelegramRequest(BaseModel):
    requester_name: str
    content: dict
    telegram_id: str