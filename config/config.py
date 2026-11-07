from datetime import timedelta
from functools import lru_cache
from pathlib import Path
from typing import Annotated
from urllib.parse import quote

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DatabaseSettings(BaseModel):
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str
    PASSWORD: str
    NAME: str = "db-plate-pulse"


class RedisSettings(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 6379
    DB: int = 0
    PASSWORD: str | None = None

    @property
    def url(self) -> str:
        if self.PASSWORD:
            password = quote(self.PASSWORD, safe="")
            return f"redis://:{password}@{self.HOST}:{self.PORT}/{self.DB}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


class ApiConfig(BaseModel):
    TITLE: str = "PlatePulse"
    DESCRIPTION: str = "Приложение для учёта, планирования меню на неделю."
    VERSION: str = "0.1.0"


class JwtConfig(BaseModel):
    ACCESS_TOKEN_LIFETIME: timedelta = timedelta(minutes=5)
    REFRESH_TOKEN_LIFETIME: timedelta = timedelta(days=1)
    ALGORITHM: str = "HS256"
    # SIGNING_KEY: str = "sectet_key_local"
    AUTH_HEADER_TYPES: str = "Bearer"


class AppSetting(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = Field(default=...)
    ALLOWED_HOSTS: Annotated[list[str], NoDecode] = []

    db: DatabaseSettings
    redis: RedisSettings = Field(default_factory=RedisSettings)
    api: ApiConfig = Field(default_factory=ApiConfig)
    jwt: JwtConfig = Field(default_factory=JwtConfig)

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def split_hosts(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [host.strip() for host in value.split(",") if host.strip()]
        return value

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )


def load_settings[SettingsT: BaseSettings](settings_cls: type[SettingsT]) -> SettingsT:
    # Required fields come from .env; calling through the BaseSettings bound keeps
    # Pyright (no pydantic-settings support) from demanding them as arguments.
    return settings_cls()


@lru_cache
def get_settings() -> AppSetting:
    return load_settings(AppSetting)


settings_env = get_settings()
