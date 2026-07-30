from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.infrastructure.database.schema.customer import CustomerSchema
from app.presentation.api.dependencies import get_handle_webhook_event_use_case
from tests.generator.customer import generate, generate_with_subscription


async def test_customer_subscription_created(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED,
            data={
                "customer": "cus-1",
                "metadata": {"customer_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"},
                "plan": {"product": "prod-1"},
            },
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.stripe_id == "cus-1"
    assert customer.stripe_product_id == "prod-1"


async def test_customer_subscription_deleted(session: AsyncSession) -> None:
    customer = generate_with_subscription()

    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED,
            data={"customer": "cus-1"},
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.stripe_product_id is None
