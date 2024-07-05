from datetime import datetime
from typing import Any, Union

from fastapi import Cookie, Depends

from . import service
from .exceptions import EmailTaken, RefreshTokenNotValid, UsernameTaken, RefreshTokenRequired
from .schemas import AuthUser, UserUpdate


async def valid_user_register_info(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()
    if await service.get_user_by_username(user.username):
        raise UsernameTaken()

    return user


async def valid_user_update_info(user: UserUpdate) -> UserUpdate:
    if user.email is not None and await service.get_user_by_email(user.email):
        raise EmailTaken()
    if user.username is not None and await service.get_user_by_username(user.username):
        raise UsernameTaken()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(None, alias="refreshToken"),
) -> dict[str, Any]:
    if not refresh_token:
        raise RefreshTokenRequired()

    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> dict[str, Any]:
    user = await service.get_user_by_id(refresh_token["user_id"])
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: dict[str, Any]) -> bool:
    return datetime.utcnow() <= db_refresh_token["expires_at"]
