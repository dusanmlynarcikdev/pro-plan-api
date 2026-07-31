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
                "customer": "customer-1",
                "metadata": {"customer_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"},
                "items": {"data": [{"price": {"product": "product-1"}}]},
            },
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.stripe_id == "customer-1"
    assert customer.stripe_product_id == "product-1"


async def test_customer_subscription_updated(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate_with_subscription()))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_UPDATED,
            data={
                "customer": "customer-1",
                "items": {"data": [{"price": {"product": "product-2"}}]},
            },
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.stripe_id == "customer-1"
    assert customer.stripe_product_id == "product-2"


async def test_customer_subscription_deleted(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate_with_subscription()))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED,
            data={"customer": "customer-1"},
        )
    )
    session.expunge_all()

    customer = (await session.exec(select(CustomerSchema))).one()

    assert customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert customer.stripe_product_id is None
