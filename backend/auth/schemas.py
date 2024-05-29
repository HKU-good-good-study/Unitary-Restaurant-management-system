import re
from enum import Enum

from pydantic import EmailStr, field_validator, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from models import CustomModel

STRONG_PASSWORD_PATTERN = re.compile(r"^(?=.*[\d])(?=.*[!@#$%^&*])[\w!@#$%^&*]{6,20}$")


class UserRole(Enum):
    MANAGER = "Manager"
    DINING_ROOM_STAFF = "Dining Room Staff"
    CUSTOMER = "Customer"
    KITCHEN_STAFF = "Kitchen Staff"


class AuthUser(CustomModel):
    username: str = Field(
        min_length=4,
        max_length=20
    )
    email: EmailStr
    password: str = Field(
        min_length=6,
        max_length=20,
    )
    phone_number: PhoneNumber
    role: UserRole
    remarks: str = Field(default="")

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )

        return password


class JWTData(CustomModel):
    user_id: str = Field(alias="sub")
    role: UserRole


class AccessTokenResponse(CustomModel):
    access_token: str
    refresh_token: str


class UserResponse(CustomModel):
    username: str
    email: EmailStr
    phone_number: PhoneNumber
    role: UserRole
    remarks: str


class UserLogIn(CustomModel):
    username: str
    password: str