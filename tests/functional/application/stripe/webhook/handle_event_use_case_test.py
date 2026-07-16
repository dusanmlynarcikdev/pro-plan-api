from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.domain.subscription.email import Email
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from app.presentation.api.dependencies import get_handle_webhook_event_use_case
from tests.functional.fake_email_sender import FakeEmailSender
from tests.generator.subscription import generate


async def test_customer_subscription_deleted(session: AsyncSession) -> None:
    subscription = generate(stripe_customer_id="cus_123")
    subscription.activate()

    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()
    session.expunge_all()

    use_case = await get_handle_webhook_event_use_case(FakeEmailSender(), session)

    await use_case(
        Event(
            type=WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED,
            data={"customer": "cus_123"},
        )
    )
    session.expunge_all()

    subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert not subscription.is_active
    assert subscription.stripe_customer_id == "cus_123"


async def test_checkout_session_completed(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    email_sender = FakeEmailSender()

    use_case = await get_handle_webhook_event_use_case(email_sender, session)

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

    assert len(email_sender.sent) == 1
    assert email_sender.sent[0].recipient == Email("john@doe.com")
    assert email_sender.sent[0].subject == "Pro plan activated"
    assert email_sender.sent[0].body == "Welcome to Pro! Your plan is now active."
