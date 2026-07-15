from functools import cache
from typing import Annotated

from pydantic import AnyUrl, HttpUrl, NameEmail, PostgresDsn, UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dist", ".env.local"), extra="ignore"
    )

    api_token: str
    database_url: PostgresDsn
    email_sender: NameEmail
    smtp_dsn: Annotated[
        AnyUrl,
        UrlConstraints(allowed_schemes=["smtp"], host_required=True),
    ]
    stripe_api_key: str
    stripe_checkout_success_url: HttpUrl
    stripe_price_id_monthly: str
    stripe_price_id_yearly: str
    stripe_webhook_secret: str


@cache
def get_config() -> Config:
    return Config()  # ty: ignore[missing-argument]
