from __future__ import annotations

import uu
import uuid
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4
from bson.objectid import ObjectId

from backend.utils import generate_random_alphanum
from .config import auth_config
from .exceptions import InvalidCredentials
from .schemas import AuthUser, UserLogIn, UserRole
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
        "created_at": datetime.utcnow(),
    }
    user_id = db.database["users"].insert_one(user_data).inserted_id
    return await db.fetch_one("users", {"_id": user_id})


async def get_user_by_id(user_id: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"_id": ObjectId(user_id)})


async def get_user_by_username(username: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"username": username})


async def get_user_by_email(email: str) -> dict[str, Any] | None:
    return await db.fetch_one("users", {"email": email})


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
    db.database["auth_refresh_token"].insert_one(token_data)
    return refresh_token


async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
    return await db.fetch_one("auth_refresh_token", {"refresh_token": refresh_token})


async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
    db.database["auth_refresh_token"].update_one(
        {"uuid": refresh_token_uuid},
        {"$set": {"expires_at": datetime.utcnow() - timedelta(days=1)}},
    )


# async def expire_refresh_token(user_id: str) -> None:
#     await db.database["auth_refresh_token"].update_one(
#         {"user_id": user_id},
#         {"$set": {"expires_at": datetime.utcnow() - timedelta(days=1)}}
#     )


async def authenticate_user(auth_data: UserLogIn) -> dict[str, Any]:
    # user = await get_user_by_email(auth_data.user)
    user = await get_user_by_username(auth_data.username)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user
