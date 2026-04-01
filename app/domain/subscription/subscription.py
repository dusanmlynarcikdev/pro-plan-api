from datetime import date
from uuid import UUID

from dateutil.relativedelta import relativedelta

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price


class Subscription:
    def __init__(self, id: UUID, email: Email, price: Price, period: Period) -> None:
        self.__id: UUID = id
        self.__email: Email = email
        self.__price: Price = price
        self.__period: Period = period
        self.__expires_at: date | None = None

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def email(self) -> Email:
        return self.__email

    @property
    def price(self) -> Price:
        return self.__price

    @property
    def period(self) -> Period:
        return self.__period

    @property
    def expires_at(self) -> date | None:
        return self.__expires_at

    def change(self, price: Price, period: Period) -> None:
        self.__price = price
        self.__period = period

    def renew(self, today: date) -> None:
        if self.expires_at is not None:
            today = self.expires_at

        match self.period:
            case Period.MONTHLY:
                self.__expires_at = today + relativedelta(months=1)
            case Period.YEARLY:
                self.__expires_at = today + relativedelta(months=12)
