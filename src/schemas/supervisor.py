from pydantic import BaseModel, EmailStr
from typing import Optional


class UserSignUp(BaseModel):
    username: str
    email: str
    position: str
    surname: str
    name: str
    patronymic: str


class RequestAssign(BaseModel):
    user_id: int
    request_id: int


class GetUserInfo(BaseModel):
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