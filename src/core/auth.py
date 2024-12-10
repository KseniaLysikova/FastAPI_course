import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from crud.auth import get_user, authenticate_user
from core.db.create_db import get_async_database
from core import errors
from models.user import User
from settings import settings


class Refresh(BaseModel):
    refresh: str


def encode_token(payload):
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')


def decode_token(token: str, token_type: str, supress: bool = False):
    try:
        data = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=['HS256'],
            options={"require": ["exp", "role", "identity"]},
        )
        if data["role"] != token_type:
            raise errors.token_validation_failed()
        return data
    except jwt.ExpiredSignatureError:
        if supress:
            return data if data["role"] == token_type else None
        raise errors.token_expired()
    except jwt.DecodeError:
        raise errors.token_validation_failed()


def set_cookie(access: str, response: Response, max_age: int):
    response.set_cookie("access", access, httponly=True, samesite="lax", max_age=max_age)


async def init_user_tokens(user: User, response: Response, db: AsyncSession):
    now = datetime.now(timezone.utc)
    identity = User.id
    max_age = settings.JWT_REFRESH_EXPIRE * 3600
    access_payload = {
        "role": "access",
        "identity": identity,
        "exp": now + timedelta(minutes=settings.JWT_REFRESH_EXPIRE)
    }
    refresh_payload = {
        "role": "refresh",
        "identity": identity,
        "exp": now + timedelta(hours=settings.JWT_REFRESH_EXPIRE)
    }
    access = encode_token(access_payload)
    refresh = encode_token(refresh_payload)
    set_cookie(access, response, max_age)
    return Refresh(refresh=refresh)


async def refresh_user_tokens(access: str, refresh: str, response: Response, db: AsyncSession):
    access_payload = decode_token(access, "access", True)
    refresh_payload = decode_token(refresh, "refresh")
    if access_payload["identity"] != refresh_payload["identity"]:
        raise errors.token_validation_failed()
    user = await get_user(db, refresh_payload["identity"])
    if user is None:
        raise errors.unauthorized()

    now = datetime.now(timezone.utc)
    identity = user.id
    max_age = settings.JWT_REFRESH_EXPIRE * 3600
    access_payload = {
        "role": "access",
        "identity": identity,
        "exp": now + timedelta(minutes=settings.JWT_REFRESH_EXPIRE)
    }
    refresh_payload = {
        "role": "refresh",
        "identity": identity,
        "exp": now + timedelta(hours=settings.JWT_REFRESH_EXPIRE)
    }
    access = encode_token(access_payload)
    refresh = encode_token(refresh_payload)
    set_cookie(access, response, max_age)
    return Refresh(refresh=refresh)


async def verify_user_access(access: str, db: AsyncSession):
    access_payload = decode_token(access, "access")
    user = await get_user(db, access_payload["identity"])

    if user is None:
        raise errors.unauthorized()

    return user


async def get_current_user(request: Request, db: AsyncSession = Depends(get_async_database)):
    access_token = request.cookies.get("Authorization")
    if access_token and access_token.startswith("Bearer "):
        access_token = access_token[len("Bearer "):]

    if not access_token:
        raise errors.unauthorized()

    try:
        payload = decode_token(access_token, "access")
        user_id = payload.get("identity")
        if user_id is None:
            raise errors.invalid_token()

        user = await get_user(db, user_id)
        if user is None:
            raise errors.user_not_found()

        return user

    except Exception:
        raise errors.invalid_credentials()
