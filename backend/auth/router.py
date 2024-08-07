from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status

from .exceptions import UserNotCreated, UserNotFound

from . import jwt, service, utils
from .dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_update_info,
    valid_user_register_info, valid_user_admin_update_info
)
from .jwt import parse_jwt_user_data, parse_jwt_customer_data, parse_jwt_admin_data
from .schemas import (
    AccessTokenResponse,
    AuthUser,
    AuthUserPasswordUpdate,
    JWTData,
    PasswordResetRequest,
    UnAuthUserPasswordReset,
    UserLogIn,
    UserResponse,
    UserUpdate, AdminUserUpdate,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/users/all", response_model=list[UserResponse])
async def get_all_users(
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
) -> list[UserResponse]:
    users = await service.get_all_users()
    return [
        UserResponse(
            username=user["username"],
            email=user["email"],
            phone_number=service.format_phone_number(user["phone_number"]),
            role=user["role"],
            remarks=user["remarks"],
        )
        for user in users
    ]


@router.post("/users/new", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    auth_data: AuthUser = Depends(valid_user_register_info),
) -> UserResponse:
    user = await service.create_user(auth_data)
    if not user:
        raise UserNotCreated()

    return UserResponse(
        username=user["username"],
        email=user["email"],
        phone_number=service.format_phone_number(user["phone_number"]),
        role=user["role"],
        remarks=user["remarks"],
    )


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    auth_data: AuthUser = Depends(valid_user_register_info),
) -> UserResponse:
    user = await service.create_user(auth_data)
    if not user:
        raise UserNotCreated()

    return UserResponse(
        username=user["username"],
        email=user["email"],
        phone_number=service.format_phone_number(user["phone_number"]),
        role=user["role"],
        remarks=user["remarks"],
    )


@router.patch("/users/username={username}", response_model=UserResponse)
async def update_user_role(
    username: str,
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
    update_data: AdminUserUpdate = Depends(valid_user_admin_update_info),
) -> UserResponse:
    user = await service.update_user_by_username(username, update_data)
    if not user:
        raise UserNotFound()

    return UserResponse(
        username=user["username"],
        email=user["email"],
        phone_number=service.format_phone_number(user["phone_number"]),
        role=user["role"],
        remarks=user["remarks"],
    )


@router.delete("/users/username={username}", status_code=204)
async def delete_user(
    username: str,
    jwt_data: JWTData = Depends(parse_jwt_admin_data),
) -> None:
    user = await service.get_user_by_username(username)
    if not user:
        raise UserNotFound()
    await service.delete_user_by_id(user["_id"])
    await service.expire_refresh_token(user["_id"])


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> UserResponse:
    user = await service.get_user_by_id(jwt_data.user_id)
    if not user:
        raise UserNotFound()

    return UserResponse(
        username=user["username"],
        email=user["email"],
        phone_number=service.format_phone_number(user["phone_number"]),
        role=user["role"],
        remarks=user["remarks"],
    )


@router.patch("/users/me", response_model=UserResponse)
async def update_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    update_data: UserUpdate = Depends(valid_user_update_info),
) -> UserResponse:
    user = await service.update_user_by_id(jwt_data.user_id, update_data)
    if not user:
        raise UserNotFound()

    return UserResponse(
        username=user["username"],
        email=user["email"],
        phone_number=service.format_phone_number(user["phone_number"]),
        role=user["role"],
        remarks=user["remarks"],
    )


@router.delete("/users/me", status_code=204)
async def delete_my_account(
    response: Response,
    jwt_data: JWTData = Depends(parse_jwt_customer_data),
) -> None:
    await service.delete_user_by_id(jwt_data.user_id)
    await service.expire_refresh_token(jwt_data.user_id)
    response.delete_cookie(
        **utils.get_access_token_settings(expired=True)
    )
    response.delete_cookie(
        **utils.get_refresh_token_settings(expired=True)
    )


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


@router.delete("/users/tokens", status_code=204)
async def logout_user(
    response: Response,
    refresh_token: dict[str, Any] = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token["uuid"])

    response.delete_cookie(
        **utils.get_access_token_settings(expired=True)
    )
    response.delete_cookie(
        **utils.get_refresh_token_settings(expired=True)
    )


@router.post("/users/password-update", status_code=204)
async def update_password(
    update_data: AuthUserPasswordUpdate,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> None:
    await service.update_user_password(jwt_data.user_id, update_data.old_password, update_data.new_password)


@router.post("/users/password-reset-token", status_code=204)
async def request_password_reset_token(
    reset_data: PasswordResetRequest,
) -> None:
    token = await service.request_password_reset_token(reset_data.email)
    print(f"Email: {reset_data.email}, Token: {token}")


@router.post("/users/password-reset", status_code=204)
async def reset_password(
    reset_data: UnAuthUserPasswordReset,
) -> None:
    await service.reset_password(reset_data.token, reset_data.new_password)
