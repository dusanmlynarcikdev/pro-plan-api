from datetime import date
from uuid import UUID

from dateutil.relativedelta import relativedelta

from app.domain.subscription.email import Email
from app.domain.subscription.errors import SubscriptionCanceled, SubscriptionExpired
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State


class Subscription:
    def __init__(self, id: UUID, email: Email, price: Price, period: Period) -> None:
        self.__id: UUID = id
        self.__email: Email = email
        self.__price: Price = price
        self.__period: Period = period
        self.__expires_at: date | None = None
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
    def expires_at(self) -> date | None:
        return self.__expires_at

    @property
    def state(self) -> State:
        return self.__state

    def change(self, price: Price, period: Period) -> None:
        self.__price = price
        self.__period = period

    def renew(self, today: date) -> None:
        if self.state == State.ACTIVE and self.expires_at is not None:
            today = self.expires_at

        match self.period:
            case Period.MONTHLY:
                self.__expires_at = today + relativedelta(months=1)
            case Period.YEARLY:
                self.__expires_at = today + relativedelta(months=12)

        self.__state = State.ACTIVE

    def cancel(self) -> None:
        """
        :raises SubscriptionCanceled:
        :raises SubscriptionExpired:
        """
        self.__check_openness()

        self.__expires_at = None
        self.__state = State.CANCELED

    def expire(self) -> None:
        """
        :raises SubscriptionCanceled:
        :raises SubscriptionExpired:
        """
        self.__check_openness()

        self.__expires_at = None
        self.__state = State.EXPIRED

    def __check_openness(self) -> None:
        """
        :raises SubscriptionCanceled:
        :raises SubscriptionExpired:
        """
        if self.__state == State.CANCELED:
            raise SubscriptionCanceled()

        if self.__state == State.EXPIRED:
            raise SubscriptionExpired()
