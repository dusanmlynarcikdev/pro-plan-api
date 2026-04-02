from datetime import date, timedelta
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
        base_date = max(today, self.expires_at or today)

        self.__expires_at = base_date + relativedelta(
            months=self.__get_period_months(),
            day=31 if self.__is_last_day_of_month(base_date) else base_date.day,
        )

    def is_active(self, today: date) -> bool:
        return self.expires_at is not None and self.expires_at >= today

    def __get_period_months(self) -> int:
        match self.period:
            case Period.MONTHLY:
                return 1
            case Period.YEARLY:
                return 12

    @staticmethod
    def __is_last_day_of_month(date: date) -> bool:
        return (date + timedelta(days=1)).day == 1
