from decimal import Decimal
from typing import Annotated
from uuid import UUID

from sqlmodel import Field

amount = Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
currency = Annotated[str, Field(min_length=3, max_length=3)]
id = Annotated[UUID, Field(primary_key=True)]
