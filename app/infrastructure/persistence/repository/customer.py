from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.customer.customer import Customer
from app.domain.customer.errors import CustomerNotFoundError
from app.infrastructure.persistence.schema.customer import CustomerSchema


class CustomerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, customer: Customer) -> None:
        self._session.add(CustomerSchema.from_domain(customer))
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()

    async def find_one_by_external_id(self, external_id: str) -> Customer | None:
        query = select(CustomerSchema).where(CustomerSchema.external_id == external_id)

        customer = (await self._session.exec(query)).one_or_none()

        return customer.to_domain() if customer else None

    async def find_one_by_stripe_id(self, stripe_id: str) -> Customer | None:
        query = select(CustomerSchema).where(CustomerSchema.stripe_id == stripe_id)

        customer = (await self._session.exec(query)).one_or_none()

        return customer.to_domain() if customer else None

    async def get(self, id: UUID) -> Customer:
        """
        :raises CustomerNotFoundError:
        """
        customer = await self._session.get(CustomerSchema, id)

        if customer is None:
            raise CustomerNotFoundError

        return customer.to_domain()

    async def get_by_external_id(self, external_id: str) -> Customer:
        """
        :raises CustomerNotFoundError:
        """
        customer = await self.find_one_by_external_id(external_id)

        if customer is None:
            raise CustomerNotFoundError

        return customer

    async def update(self, customer: Customer) -> None:
        _customer = await self._session.get(CustomerSchema, customer.id)

        if _customer is None:
            raise RuntimeError("Customer not found")

        _customer.update_from_domain(customer)
        await self._session.flush()
