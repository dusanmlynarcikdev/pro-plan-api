from functools import lru_cache
from typing import Annotated

from pydantic import AnyUrl, NameEmail, PostgresDsn, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.dist", extra="ignore")

    api_key: str
    database_url: PostgresDsn
    email_sender: NameEmail
    smtp_dsn: Annotated[
        AnyUrl,
        UrlConstraints(allowed_schemes=["smtp"], host_required=True),
    ]


@lru_cache
def get_config() -> Config:
    return Config()  # ty: ignore[missing-argument]
