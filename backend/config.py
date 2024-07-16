from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    HOST: str = "http://localhost"
    PORT: int = 8000

    FRONTEND_HOST: str = "http://localhost"
    FRONTEND_PORT: int = 5173


app_config = AppConfig()
