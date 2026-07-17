from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.infrastructure.persistence.schema.customer import CustomerSchema
from app.presentation.api.dependencies import get_handle_webhook_event_use_case
from tests.generator.customer import generate


async def test_customer_subscription_deleted(session: AsyncSession) -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")

    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED,
            data={"customer": "cus_123"},
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert not customer.has_pro
    assert customer.stripe_id == "cus_123"


async def test_checkout_session_completed(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

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

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.has_pro
    assert customer.stripe_id == "cus_123"
