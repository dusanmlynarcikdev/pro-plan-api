from uuid import uuid7

from app.domain.customer.customer import Customer
from app.domain.customer.email import Email
from app.domain.customer.repository import CustomerRepository


class GetOrCreateCustomerUseCase:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository: CustomerRepository = repository

    async def __call__(self, email: Email) -> Customer:
        customer = await self._repository.find_one_by_email(email)

        if customer is None:
            customer = Customer(uuid7(), email)
            await self._repository.add(customer)
            await self._repository.commit()

        return customer
