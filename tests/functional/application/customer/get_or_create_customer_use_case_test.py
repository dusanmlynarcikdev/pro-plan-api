from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.customer.get_or_create_customer_use_case import (
    GetOrCreateCustomerUseCase,
)
from app.domain.customer.email import Email
from app.infrastructure.persistence.repository.customer import (
    CustomerRepository,
)
from app.infrastructure.persistence.schema.customer import CustomerSchema
from tests.generator.customer import generate


async def test_create(session: AsyncSession) -> None:
    use_case = GetOrCreateCustomerUseCase(CustomerRepository(session))

    customer = await use_case(Email("john@doe.com"))
    session.expunge_all()

    assert customer.email.value == "john@doe.com"
    assert not customer.has_pro
    assert customer.stripe_id is None

    repository_customer = (await session.exec(select(CustomerSchema))).one()

    assert repository_customer.id == customer.id
    assert repository_customer.email == "john@doe.com"
    assert not repository_customer.has_pro
    assert repository_customer.stripe_id is None


async def test_create_when_another_customer_exists(
    session: AsyncSession,
) -> None:
    session.add(CustomerSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    use_case = GetOrCreateCustomerUseCase(CustomerRepository(session))

    customer = await use_case(Email("john2@doe.com"))
    session.expunge_all()

    assert customer.id != UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")

    repository_customers = (await session.exec(select(CustomerSchema))).all()

    assert len(repository_customers) == 2
    assert repository_customers[0].id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_customers[1].id == customer.id
