"""应用配置读取。"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.constant import (
    DEFAULT_DB_PATH,
    DEFAULT_HTTP_TIMEOUT_SECONDS,
    DEFAULT_USER_AGENT,
)


class Settings(BaseSettings):
    """本地宏观监控配置。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    macro_db_path: Path = Field(default=DEFAULT_DB_PATH, alias="MACRO_DB_PATH")
    fred_api_key: str | None = Field(default=None, alias="FRED_API_KEY")
    macro_http_timeout_seconds: int = Field(
        default=DEFAULT_HTTP_TIMEOUT_SECONDS,
        alias="MACRO_HTTP_TIMEOUT_SECONDS",
    )
    macro_user_agent: str = Field(default=DEFAULT_USER_AGENT, alias="MACRO_USER_AGENT")


def get_settings() -> Settings:
    """返回当前运行配置。"""

    return Settings()
