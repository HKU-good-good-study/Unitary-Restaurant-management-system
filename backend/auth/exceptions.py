from .constants import ErrorCode
from backend.exceptions import (
    DetailedHTTPException,
    NotFound,
    BadRequest,
    NotAuthenticated,
    PermissionDenied,
)


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class EmailTaken(BadRequest):
    DETAIL = ErrorCode.EMAIL_TAKEN


class UsernameTaken(BadRequest):
    DETAIL = ErrorCode.USERNAME_TAKEN


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID


class UserNotFound(NotFound):
    DETAIL = ErrorCode.USER_NOT_FOUND


class UserNotCreated(DetailedHTTPException):
    DETAIL = ErrorCode.USER_NOT_CREATED
