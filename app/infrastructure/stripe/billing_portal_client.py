import logging

from stripe import StripeClient, StripeError
from stripe.params.billing_portal import SessionCreateParams

from app.application.stripe.errors import UnableToCreateBillingPortalSessionError

logger = logging.getLogger(__name__)


class BillingPortalClient:
    def __init__(self, client: StripeClient) -> None:
        self._client = client

    async def create_session(self, customer_id: str) -> str:
        try:
            session = await self._client.v1.billing_portal.sessions.create_async(
                SessionCreateParams(customer=customer_id)
            )
        except StripeError as e:
            logger.error(e.user_message)
            raise UnableToCreateBillingPortalSessionError

        return session.url
