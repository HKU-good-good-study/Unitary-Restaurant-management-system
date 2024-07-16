from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any, Union

from pydantic import UUID4
from bson.objectid import ObjectId

from utils import generate_random_alphanum
from .config import auth_config
from .exceptions import InvalidCredentials, InvalidEmail, InvalidResetToken, PasswordNotMatched, ResetTokenExpired
from .schemas import AuthUser, UserLogIn, UserRole, UserUpdate, AdminUserUpdate
from .security import check_password, hash_password
from database import Database

db = Database()  # Create an instance of the Database class


async def create_user(user: AuthUser) -> dict[str, Any] | None:
    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password),
        "phone_number": user.phone_number,
        "role": user.role.value if isinstance(user.role, UserRole) else user.role,
        "remarks": user.remarks,
        "created_at": datetime.utcnow().replace(microsecond=0),
    }
    user_id = await db.execute("users", user_data, "insert")
    return await db.fetch_one("users", {"_id": user_id.inserted_id})


async def get_user_by_id(user_id: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"_id": ObjectId(user_id)})


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"username": username})


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"email": email})


async def get_user_by_phone_number(phone_number: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"phone_number": phone_number})


async def get_all_users() -> list[dict[str, Any]]:
    return await db.fetch_all("users", {})


async def update_user_by_id(user_id: str, update_data: Union[UserUpdate, AdminUserUpdate]) -> dict[str, Any] | None:
    update_data = update_data.model_dump(exclude_none=True)
    await db.execute(
        "users",
        {"filter": {"_id": ObjectId(user_id)}, "update": {"$set": update_data}},
        "update"
    )
    return await db.fetch_one("users", {"_id": ObjectId(user_id)})


async def update_user_by_username(
    username: str,
    update_data: Union[UserUpdate, AdminUserUpdate]
) -> dict[str, Any] | None:
    update_data = update_data.model_dump(exclude_none=True)
    if "role" in update_data:
        update_data["role"] = update_data["role"].value
    await db.execute(
        "users",
        {"filter": {"username": username}, "update": {"$set": update_data}},
        "update"
    )
    return await db.fetch_one("users", {"username": username}
                              )


async def delete_user_by_id(user_id: str) -> None:
    await db.execute("users", {"_id": ObjectId(user_id)}, "delete")


async def create_refresh_token(
    *, user_id: str, refresh_token: str | None = None
) -> str:
    if not refresh_token:
        refresh_token = generate_random_alphanum(64)

    token_data = {
        "uuid": uuid.uuid4(),
        "refresh_token": refresh_token,
        "expires_at": datetime.utcnow()
                      + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
        "user_id": user_id,
    }
    await db.execute("auth_refresh_token", token_data, "insert")
    return refresh_token


async def create_password_reset_token(
    user_id: str, reset_token: str | None = None
) -> str:
    if not reset_token:
        reset_token = generate_random_alphanum(64)

    token_data = {
        "uuid": uuid.uuid4(),
        "reset_token": reset_token,
        "expires_at": datetime.utcnow()
                      + timedelta(seconds=auth_config.RESET_TOKEN_EXP),
        "user_id": user_id,
    }
    await db.execute("auth_reset_token", token_data, "insert")
    return reset_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    return await db.fetch_one("auth_refresh_token", {"refresh_token": refresh_token})


async def get_password_reset_token(reset_token: str) -> dict[str, Any] | None:
    return await db.fetch_one("auth_reset_token", {"reset_token": reset_token})


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    await db.execute(
        "auth_refresh_token",
        {"filter": {"uuid": refresh_token_uuid},
         "update": {"$set": {"expires_at": datetime.utcnow() - timedelta(days=1)}}},
        "update"
    )


async def expire_reset_token(reset_token_uuid: UUID4) -> None:
    await db.execute(
        "auth_reset_token",
        {"filter": {"uuid": reset_token_uuid},
         "update": {"$set": {"expires_at": datetime.utcnow() - timedelta(days=1)}}},
        "update"
    )


# async def expire_refresh_token_by_user_id(user_id: str) -> None:
#     await db.execute(
#         "auth_refresh_token",
#         {"filter": {"user_id": user_id},
#          "update": {"$set": {"expires_at": datetime.utcnow() - timedelta(days=1)}}},
#         "update"
#     )


async def authenticate_user(auth_data: UserLogIn) -> dict[str, Any]:
    # user = await get_user_by_email(auth_data.user)
    user = await get_user_by_username(auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user


async def verify_password(user_id: str, old_password: str) -> bool:
    user = await get_user_by_id(user_id)
    if not user:
        raise InvalidCredentials()

    return check_password(old_password, user["password"])


async def change_password(user_id: str, new_password: str) -> None:
    await db.execute(
        "users",
        {"filter": {"_id": ObjectId(user_id)},
         "update": {"$set": {"password": hash_password(new_password)}}},
        "update"
    )


async def update_user_password(user_id: str, old_password: str, new_password: str) -> None:
    if not await verify_password(user_id, old_password):
        raise PasswordNotMatched()

    await change_password(user_id, new_password)


async def request_password_reset_token(email: str) -> str:
    user = await get_user_by_email(email)
    if not user:
        raise InvalidEmail()

    reset_token = generate_random_alphanum(64)
    reset_token = await create_password_reset_token(user_id=str(user["_id"]), reset_token=reset_token)
    # send_reset_password_email(user["email"], reset_token)
    return reset_token


async def reset_password(reset_token: str, new_password: str) -> None:
    reset_token_data = await get_password_reset_token(reset_token)
    if not reset_token_data:
        raise InvalidResetToken()
    if reset_token_data["expires_at"] < datetime.utcnow():
        raise ResetTokenExpired()

    await change_password(reset_token_data["user_id"], new_password)
    await expire_reset_token(reset_token_data["uuid"])

    # send_password_reset_email(user["email"])


def format_phone_number(phone_number: str) -> str:
    if phone_number.startswith("tel:"):
        phone_number = phone_number[4:]

    parts = phone_number.split("-", 1)
    formatted_number = parts[0] + " " + parts[1].replace("-", "") if len(parts) > 1 else parts[0]

    return formatted_number
