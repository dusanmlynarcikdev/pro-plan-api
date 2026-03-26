from decimal import Decimal

from pydantic_extra_types.currency_code import ISO4217
from sqlmodel import SQLModel


class Price(SQLModel):
    amount: Decimal
    currency: ISO4217
