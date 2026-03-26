from dataclasses import dataclass
from decimal import Decimal

from pydantic import TypeAdapter, ValidationError
from pydantic_extra_types.currency_code import ISO4217

from app.domain.subscription.errors import InvalidAmount, InvalidCurrency

_CURRENCY_TYPE_ADAPTER = TypeAdapter(ISO4217)


@dataclass(frozen=True, slots=True)
class Price:
    amount: Decimal
    currency: str

    def __post_init__(self) -> None:
        if self.amount <= 0:
            raise InvalidAmount()

        try:
            _CURRENCY_TYPE_ADAPTER.validate_python(self.currency)
        except ValidationError:
            raise InvalidCurrency()
