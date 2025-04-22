from authx import AuthX, AuthXConfig
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = "./backend/api/security/.env"


def get_authx_config() -> AuthXConfig:
    settings = Settings()
    config = AuthXConfig()
    
    config.JWT_SECRET_KEY = settings.JWT_SECRET_KEY
    config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
    config.JWT_TOKEN_LOCATION = ["cookies"]
    config.JWT_ALGORITHM = settings.JWT_ALGORITHM
    return config

security = AuthX(config=get_authx_config())

__all__ = ["security"]