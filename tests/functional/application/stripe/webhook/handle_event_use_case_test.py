from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.application.stripe.webhook.handle_event_use_case import HandleEventUseCase
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate


async def test_checkout_session_completed(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    use_case = HandleEventUseCase(SubscriptionRepository(session))

    await use_case(
        Event(
            type=WebhookEventType.CHECKOUT_SESSION_COMPLETED,
            data={
                "client_reference_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04",
                "customer": "cus_123",
            },
        )
    )
    session.expunge_all()

    subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert subscription.is_active
    assert subscription.stripe_customer_id == "cus_123"
