from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.payment.payment import Payment
from app.domain.subscription.price import Price
from app.infrastructure.persistence.repository.payment import PaymentRepository
from app.infrastructure.persistence.schema.payment import PaymentSchema
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.payment import generate
from tests.generator.subscription import generate as generate_subscription


async def test_add(session: AsyncSession) -> None:
    subscription = generate_subscription()
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()

    await PaymentRepository(session).add(generate())
    session.expunge_all()

    result = await session.exec(select(PaymentSchema))
    repository_payment = result.one()

    assert repository_payment.id == UUID("019d3e91-911c-7f71-80ce-276ef0cff36e")
    assert repository_payment.subscription_id == subscription.id
    assert repository_payment.amount == Decimal("1")
    assert repository_payment.currency == "USD"
    assert repository_payment.paid_at == date(2026, 1, 1)


async def test_find_by_subscription_id(session: AsyncSession) -> None:
    subscription = generate_subscription()
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()

    payment1 = generate()
    payment2 = generate(
        UUID("019d3ea9-e070-7c88-ad30-c3a3f6a61730"),
        Price(Decimal("2"), "EUR"),
        date(2026, 1, 2),
    )
    session.add(PaymentSchema.from_domain(payment1))
    session.add(PaymentSchema.from_domain(payment2))
    await session.flush()
    session.expunge_all()

    repository_payments = await get_payments(session)

    assert len(repository_payments) == 2

    assert repository_payments[0].id == payment2.id
    assert repository_payments[0].subscription_id == subscription.id
    assert repository_payments[0].price.amount == payment2.price.amount
    assert repository_payments[0].price.currency == payment2.price.currency
    assert repository_payments[0].paid_at == payment2.paid_at

    assert repository_payments[1].id == payment1.id
    assert repository_payments[1].subscription_id == subscription.id
    assert repository_payments[1].price.amount == payment1.price.amount
    assert repository_payments[1].price.currency == payment1.price.currency
    assert repository_payments[1].paid_at == payment1.paid_at


async def test_find_by_subscription_id_with_offset_one(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate_subscription()))
    await session.flush()

    payment = generate()
    session.add(PaymentSchema.from_domain(payment))
    session.add(
        PaymentSchema.from_domain(
            generate(UUID("019d3ea9-e070-7c88-ad30-c3a3f6a61730"))
        )
    )
    await session.flush()
    session.expunge_all()

    repository_payments = await get_payments(session, offset=1)

    assert len(repository_payments) == 1
    assert repository_payments[0].id == payment.id


async def test_find_by_subscription_id_payment_for_another_subscription(
    session: AsyncSession,
) -> None:
    session.add(SubscriptionSchema.from_domain(generate_subscription()))
    await session.flush()

    session.add(PaymentSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_payments = await get_payments(
        session, UUID("019d3ea9-e070-7c88-ad30-c3a3f6a61730")
    )

    assert len(repository_payments) == 0


async def test_find_by_subscription_id_no_payments(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate_subscription()))
    await session.flush()
    session.expunge_all()

    repository_payments = await get_payments(session)

    assert len(repository_payments) == 0


async def test_find_by_subscription_id_no_subscription(
    session: AsyncSession,
) -> None:
    repository_payments = await get_payments(session)

    assert len(repository_payments) == 0


async def get_payments(
    session: AsyncSession,
    subscription_id: UUID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    offset: int = 0,
) -> list[Payment]:
    return [
        payment
        async for payment in PaymentRepository(session).find_by_subscription_id(
            subscription_id, offset
        )
    ]
