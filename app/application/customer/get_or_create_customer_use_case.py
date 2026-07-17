from uuid import uuid7

from app.domain.customer.customer import Customer
from app.domain.customer.repository import CustomerRepository


class GetOrCreateCustomerUseCase:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository: CustomerRepository = repository

    async def __call__(self, external_id: str) -> Customer:
        customer = await self._repository.find_one_by_external_id(external_id)

        if customer is None:
            customer = Customer(uuid7(), external_id)
            await self._repository.add(customer)
            await self._repository.commit()

        return customer
