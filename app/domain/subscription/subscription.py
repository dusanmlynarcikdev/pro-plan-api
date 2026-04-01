from datetime import date
from uuid import UUID

from dateutil.relativedelta import relativedelta

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period


class Subscription:
    def __init__(self, id: UUID, email: Email, period: Period) -> None:
        self.__id: UUID = id
        self.__email: Email = email
        self.period: Period = period
        self.__expires_at: date | None = None

    @property
    def id(self) -> UUID:
        return self.__id

    @property
    def email(self) -> Email:
        return self.__email

    @property
    def expires_at(self) -> date | None:
        return self.__expires_at

    def renew(self, today: date) -> None:
        if self.expires_at is not None:
            today = self.expires_at

        match self.period:
            case Period.MONTHLY:
                self.__expires_at = today + relativedelta(months=1)
            case Period.YEARLY:
                self.__expires_at = today + relativedelta(months=12)
