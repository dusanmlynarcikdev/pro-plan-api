from functools import lru_cache
from typing import Annotated

from pydantic import AnyUrl, NameEmail, PostgresDsn, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dist", extra="ignore")

    database_url: PostgresDsn
    email_sender: NameEmail
    smtp_dsn: Annotated[
        AnyUrl,
        UrlConstraints(allowed_schemes=["smtp"], host_required=True),
    ]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # ty: ignore[missing-argument]
