from functools import cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.dist", ".env.local"), extra="ignore"
    )

    database_url: PostgresDsn
    stripe_api_key: str
    stripe_price_id_monthly: str
    stripe_price_id_yearly: str
    stripe_webhook_secret: str


@cache
def get_config() -> Config:
    return Config()  # ty: ignore[missing-argument]
