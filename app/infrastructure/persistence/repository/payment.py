from typing import AsyncIterator
from uuid import UUID

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.payment.payment import Payment
from app.infrastructure.persistence.schema.payment import PaymentSchema


class PaymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, payment: Payment) -> None:
        self.session.add(PaymentSchema.from_domain(payment))
        await self.session.flush()

    async def find_by_subscription_id(
        self, subscription_id: UUID, offset: int
    ) -> AsyncIterator[Payment]:
        query = (
            select(PaymentSchema)
            .where(PaymentSchema.subscription_id == subscription_id)
            .order_by(desc(PaymentSchema.paid_at), desc(PaymentSchema.id))
            .offset(offset)
            .limit(10)
        )

        result = await self.session.stream(query)

        async for payment in result.scalars():
            yield payment.to_domain()
