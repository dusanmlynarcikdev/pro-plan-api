from app.domain.customer.customer import Customer
from app.domain.customer.email import Email
from app.domain.customer.repository import CustomerRepository


class GetCustomerUseCase:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository: CustomerRepository = repository

    async def __call__(self, email: Email) -> Customer:
        """
        :raises CustomerNotFound:
        """
        return await self._repository.get_by_email(email)
