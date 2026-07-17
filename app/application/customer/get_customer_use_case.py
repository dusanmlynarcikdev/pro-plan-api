from app.domain.customer.customer import Customer
from app.domain.customer.repository import CustomerRepository


class GetCustomerUseCase:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository: CustomerRepository = repository

    async def __call__(self, external_id: str) -> Customer:
        """
        :raises CustomerNotFound:
        """
        return await self._repository.get_by_external_id(external_id)
