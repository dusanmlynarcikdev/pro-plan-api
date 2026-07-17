from typing import Protocol
from uuid import UUID

from app.domain.customer.customer import Customer


class CustomerRepository(Protocol):
    async def add(self, customer: Customer) -> None: ...

    async def commit(self) -> None: ...

    async def find_one_by_external_id(self, external_id: str) -> Customer | None: ...

    async def find_one_by_stripe_id(self, stripe_id: str) -> Customer | None: ...

    async def get(self, id: UUID) -> Customer:
        """
        :raises CustomerNotFound:
        """
        ...

    async def get_by_external_id(self, external_id: str) -> Customer:
        """
        :raises CustomerNotFound:
        """
        ...

    async def update(self, customer: Customer) -> None: ...
