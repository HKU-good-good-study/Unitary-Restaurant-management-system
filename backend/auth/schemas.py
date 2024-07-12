import re
from enum import Enum
from typing import Optional

from pydantic import EmailStr, field_validator, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,20}$")


class UserRole(Enum):
    MANAGER = "Manager"
    DINING_ROOM_STAFF = "Dining Room Staff"
    CUSTOMER = "Customer"
    KITCHEN_STAFF = "Kitchen Staff"


class User(CustomModel):
    username: str = Field(min_length=4, max_length=20)
    email: EmailStr
    phone_number: PhoneNumber
    role: UserRole
    remarks: str = Field(default="")


class AuthUser(User):
    password: str = Field(
        min_length=6,
        max_length=20,
    )

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least one lower character, "
                "one upper character, a digit or a special symbol"
            )

        return password


class UserResponse(User):
    phone_number: str


class UserUpdate(CustomModel):
    username: Optional[str] = Field(None, min_length=4, max_length=20)
    email: Optional[EmailStr] = None
    phone_number: Optional[PhoneNumber] = None
    remarks: Optional[str] = None


class AdminUserUpdate(UserUpdate):
    role: Optional[UserRole] = None


class PasswordUpdate(CustomModel):
    new_password: str = Field(
        min_length=6,
        max_length=20,
    )

    @field_validator("new_password", mode="after")
    @classmethod
    def valid_new_password(cls, new_password):
        if not re.match(STRONG_PASSWORD_PATTERN, new_password):
            raise ValueError(
                "Password must contain at least one lower character, "
                "one upper character, a digit or a special symbol"
            )
        return new_password


class AuthUserPasswordUpdate(PasswordUpdate):
    old_password: str


class PasswordResetRequest(CustomModel):
    email: EmailStr


class UnAuthUserPasswordReset(PasswordUpdate):
    token: str


class JWTData(CustomModel):
    user_id: str = Field(alias="sub")
    role: UserRole


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserLogIn(CustomModel):
    username: str
    password: str
