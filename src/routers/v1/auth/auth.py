from fastapi import APIRouter, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core import errors
from core.db.create_db import get_async_database
from core.auth import init_user_tokens, refresh_user_tokens, authenticate_user
from schemas.auth import LoginRequest, LoginResponse, RefreshTokenRequest, RefreshTokenResponse

router = APIRouter()


@router.post("/login",
             response_model=LoginResponse,
             responses=errors.with_errors())
async def login(login_data: LoginRequest, response: Response,
                db: AsyncSession = Depends(get_async_database)):
    user = await authenticate_user(login_data.username, login_data.password, db)
    if not user:
        raise errors.unauthorized()

    tokens = await init_user_tokens(user, response, db)
    return LoginResponse(tokens.refresh)


@router.post("/refresh_token",
             response_model=RefreshTokenResponse,
             responses=errors.with_errors())
async def refresh_token(refresh_data: RefreshTokenRequest,
                        response: Response, db: AsyncSession = Depends(get_async_database)):
    tokens = await refresh_user_tokens(refresh_data.access_token,
                                       refresh_data.refresh_token, response, db)
    return RefreshTokenResponse(tokens.refresh)


@router.post("/logout",
             status_code=204,
             responses=errors.with_errors())
async def logout(response: Response):
    response.delete_cookie("access")
