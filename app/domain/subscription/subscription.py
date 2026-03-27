from datetime import date
from uuid import UUID

from dateutil.relativedelta import relativedelta

from app.domain.subscription.email import Email
from app.domain.subscription.errors import SubscriptionExpired
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State


class Subscription:
    def __init__(self, id: UUID, email: Email, price: Price, period: Period) -> None:
        self.__id: UUID = id
        self.__email: Email = email
        self.__price: Price = price
        self.__period: Period = period
        self.__next_payment_date: date | None = None
        self.__state: State = State.NEW

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
    def next_payment_date(self) -> date | None:
        return self.__next_payment_date

    @property
    def state(self) -> State:
        return self.__state

    def change(self, price: Price, period: Period) -> None:
        """
        :raises SubscriptionExpired:
        """
        self.__check_expiration()

        self.__price = price
        self.__period = period

    def renew(self, payment_date: date) -> None:
        if self.state == State.ACTIVE and self.next_payment_date is not None:
            payment_date = self.next_payment_date

        match self.period:
            case Period.MONTHLY:
                self.__next_payment_date = payment_date + relativedelta(months=1)
            case Period.YEARLY:
                self.__next_payment_date = payment_date + relativedelta(months=12)

        self.__state = State.ACTIVE

    def expire(self) -> None:
        """
        :raises SubscriptionExpired:
        """
        self.__check_expiration()

        self.__next_payment_date = None
        self.__state = State.EXPIRED

    def __check_expiration(self) -> None:
        """
        :raises SubscriptionExpired:
        """
        if self.__state == State.EXPIRED:
            raise SubscriptionExpired()
