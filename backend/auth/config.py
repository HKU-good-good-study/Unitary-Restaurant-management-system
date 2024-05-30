from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 60 * 60

    ACCESS_TOKEN_KEY: str = "accessToken"
    REFRESH_TOKEN_KEY: str = "refreshToken"
    REFRESH_TOKEN_EXP: int = 60 * 60 * 24 * 21

    SECURE_COOKIES: bool = True


auth_config = AuthConfig(JWT_ALG="HS256", JWT_SECRET="secret")
