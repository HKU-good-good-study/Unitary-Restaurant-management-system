from __future__ import annotations

from datetime import datetime, timedelta
import traceback
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import auth_config
from .exceptions import AuthorizationFailed, AuthRequired, InvalidToken
from .schemas import JWTData, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/tokens", auto_error=False)

# Define the access levels for each role
ACCESS_LEVELS = {
    UserRole.MANAGER: 3,
    UserRole.KITCHEN_STAFF: 2,
    UserRole.DINING_ROOM_STAFF: 1,
    UserRole.CUSTOMER: 0,
}


def has_access(required_role: UserRole, user_role: UserRole) -> bool:
    return ACCESS_LEVELS[user_role] >= ACCESS_LEVELS[required_role]


def create_access_token(
        *,
        user: dict[str, Any],
        expires_delta: timedelta = timedelta(minutes=auth_config.JWT_EXP),
) -> str:
    jwt_data = {
        "sub": str(user["_id"]),
        "exp": datetime.utcnow() + expires_delta,
        "role": user["role"],
    }

    return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)


async def parse_jwt_user_data_optional(
        token: str = Depends(oauth2_scheme),
) -> JWTData | None:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, auth_config.JWT_SECRET, algorithms=[auth_config.JWT_ALG]
        )
    except JWTError:
        print(traceback.format_exc())
        raise InvalidToken()

    return JWTData(**payload)


async def parse_jwt_user_data(
        token: JWTData | None = Depends(parse_jwt_user_data_optional),
) -> JWTData:
    if not token:
        raise AuthRequired()

    return token


async def parse_jwt_admin_data(
        token: JWTData = Depends(parse_jwt_user_data),
        required_role: UserRole = UserRole.MANAGER,
) -> JWTData:
    if not has_access(required_role, token.role):
        raise AuthorizationFailed()

    return token


async def validate_admin_access(
        token: JWTData | None = Depends(parse_jwt_user_data_optional),
        required_role: UserRole = UserRole.MANAGER,
) -> None:
    if token and has_access(required_role, token.role):
        return

    raise AuthorizationFailed()
