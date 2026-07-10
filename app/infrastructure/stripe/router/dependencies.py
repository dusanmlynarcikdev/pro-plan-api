from typing import Annotated

from fastapi import Depends

from app.infrastructure.stripe.client.client import Client
from app.presentation.api.dependencies import Config


async def get_stripe_client(config: Config) -> Client:
    return Client(config.stripe_api_key)


StripeClient = Annotated[Client, Depends(get_stripe_client)]
