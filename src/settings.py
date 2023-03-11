from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_host: str
    database_port: str
    database_name: str

    class Config:
        env_file = ".env"


class JWTSettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


@lru_cache()
def settings():
    return Settings()


@lru_cache()
def jwtsettings():
    return JWTSettings()
