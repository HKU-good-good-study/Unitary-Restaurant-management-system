from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from .exceptions import UserNotCreated, UserNotFound

from . import jwt, service, utils
from .dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from .jwt import parse_jwt_user_data
from .schemas import AccessTokenResponse, AuthUser, JWTData, UserLogIn, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_create),
) -> dict[str, str]:
    user = await service.create_user(auth_data)
    if not user:
        raise UserNotCreated()

    return {
        "username": user["username"],
        "email": user["email"],
        "phone_number": user["phone_number"],
        "role": user["role"],
        "remarks": user["remarks"],
    }


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user = await service.get_user_by_id(jwt_data.user_id)
    if not user:
        raise UserNotFound()

    return {
        "username": user["username"],
        "email": user["email"],
        "phone_number": user["phone_number"],
        "role": user["role"],
        "remarks": user["remarks"],
    }


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(auth_data: UserLogIn, response: Response) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    access_token_value = jwt.create_access_token(user=user)
    refresh_token_value = await service.create_refresh_token(user_id=user["_id"])

    response.set_cookie(**utils.get_access_token_settings(access_token_value))
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=access_token_value,
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
    worker: BackgroundTasks,
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
    user: dict[str, Any] = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token["user_id"]
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token["uuid"])
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_access_token_settings("", expired=True)
    )
    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
