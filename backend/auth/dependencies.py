from datetime import datetime
from typing import Any, Union

from fastapi import Cookie, Depends

from . import service
from .exceptions import EmailTaken, RefreshTokenNotValid, UsernameTaken, RefreshTokenRequired, PhoneTaken
from .schemas import AuthUser, UserUpdate, AdminUserUpdate


async def validate_user_info(
    user_data: Union[AuthUser, UserUpdate, AdminUserUpdate],
    validation_type: str
) -> Union[AuthUser, UserUpdate, AdminUserUpdate]:
    # Check for email existence if present in user_data
    if hasattr(user_data, 'email') and user_data.email is not None:
        if await service.get_user_by_email(user_data.email):
            raise EmailTaken()

    # Check for username existence if present in user_data
    if hasattr(user_data, 'username') and user_data.username is not None:
        if await service.get_user_by_username(user_data.username):
            raise UsernameTaken()

    # Check for phone number existence if present in user_data
    if hasattr(user_data, 'phone_number') and user_data.phone_number is not None:
        if await service.get_user_by_phone_number(user_data.phone_number):
            raise PhoneTaken()

    return user_data


# Update the dependent functions to use this streamlined approach
async def valid_user_register_info(user: AuthUser) -> AuthUser:
    return await validate_user_info(user, 'register')


async def valid_user_update_info(user: UserUpdate) -> UserUpdate:
    return await validate_user_info(user, 'update')


async def valid_user_admin_update_info(user: AdminUserUpdate) -> AdminUserUpdate:
    return await validate_user_info(user, 'admin_update')


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
