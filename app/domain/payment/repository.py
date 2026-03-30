from typing import AsyncIterator, Protocol
from uuid import UUID

from app.domain.payment.payment import Payment


class PaymentRepository(Protocol):
    async def add(self, payment: Payment) -> None: ...

    async def find_by_subscription_id(
        self, subscription_id: UUID, offset: int
    ) -> AsyncIterator[Payment]: ...
