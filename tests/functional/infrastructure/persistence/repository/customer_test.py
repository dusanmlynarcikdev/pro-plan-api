from uuid import UUID

from pytest import raises
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.customer.email import Email
from app.domain.customer.errors import CustomerNotFoundError
from app.infrastructure.persistence.repository.customer import (
    CustomerRepository,
)
from app.infrastructure.persistence.schema.customer import CustomerSchema
from tests.generator.customer import generate


async def test_add(session: AsyncSession) -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")

    await CustomerRepository(session).add(customer)
    session.expunge_all()

    repository_customer = await get_customer(session)

    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_customer.email == "john@doe.com"
    assert repository_customer.has_pro
    assert repository_customer.stripe_id == "cus_123"


async def test_add_duplicity(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with raises(IntegrityError, match="c_ui_email"):
        async with session.begin_nested():
            await CustomerRepository(session).add(
                generate(UUID("019d2fc4-e06a-7dce-a23c-b8ce364f46a2"))
            )


async def test_find_one_by_email(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).find_one_by_email(
        Email("john@doe.com")
    )

    assert repository_customer is not None
    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


async def test_find_one_by_email_another_customer_exists(
    session: AsyncSession,
) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).find_one_by_email(
        Email("john2@doe.com")
    )

    assert repository_customer is None


async def test_find_one_by_email_empty_repository(
    session: AsyncSession,
) -> None:
    repository_customer = await CustomerRepository(session).find_one_by_email(
        Email("john@doe.com")
    )

    assert repository_customer is None


async def test_find_one_by_stripe_id(session: AsyncSession) -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")

    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).find_one_by_stripe_id(
        "cus_123"
    )

    assert repository_customer is not None
    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


async def test_find_one_by_stripe_id_another_customer_exists(
    session: AsyncSession,
) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).find_one_by_stripe_id(
        "cus_456"
    )

    assert repository_customer is None


async def test_find_one_by_stripe_id_empty_repository(
    session: AsyncSession,
) -> None:
    repository_customer = await CustomerRepository(session).find_one_by_stripe_id(
        "cus_456"
    )

    assert repository_customer is None


async def test_get(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).get(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    )

    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


async def test_get_another_customer_exists(
    session: AsyncSession,
) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with raises(CustomerNotFoundError):
        await CustomerRepository(session).get(
            UUID("019f652b-1a7b-7a4a-8be3-e736be31fede")
        )


async def test_get_empty_repository(session: AsyncSession) -> None:
    with raises(CustomerNotFoundError):
        await CustomerRepository(session).get(
            UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
        )


async def test_get_by_email(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_customer = await CustomerRepository(session).get_by_email(
        Email("john@doe.com")
    )

    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


async def test_get_by_email_another_customer_exists(
    session: AsyncSession,
) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with raises(CustomerNotFoundError):
        await CustomerRepository(session).get_by_email(Email("john2@doe.com"))


async def test_get_by_email_empty_repository(session: AsyncSession) -> None:
    with raises(CustomerNotFoundError):
        await CustomerRepository(session).get_by_email(Email("john@doe.com"))


async def test_update(session: AsyncSession) -> None:
    customer = generate()
    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    customer.link_stripe_subscription("cus_123")

    await CustomerRepository(session).update(customer)
    session.expunge_all()

    repository_customer = await get_customer(session)

    assert repository_customer.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_customer.has_pro
    assert repository_customer.stripe_id == "cus_123"


async def test_update_unknown(session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with raises(RuntimeError, match="Customer not found"):
        await CustomerRepository(session).update(
            generate(UUID("019d2fb0-b4d2-7731-9924-9de4130ec63e"))
        )


async def get_customer(session: AsyncSession) -> CustomerSchema:
    result = await session.exec(select(CustomerSchema))

    return result.one()
