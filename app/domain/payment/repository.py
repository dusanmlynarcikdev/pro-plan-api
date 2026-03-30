from typing import AsyncIterator, Protocol

from .payment import Payment


class PaymentRepository(Protocol):
    async def add(self, payment: Payment) -> None: ...

    async def find_by_subscription_id(
        self, subscription_id: str, offset: int
    ) -> AsyncIterator[Payment]: ...

    async def find_one_by_subscription_id_and_date(
        self, subscription_id: str, date: str
    ) -> Payment | None: ...
