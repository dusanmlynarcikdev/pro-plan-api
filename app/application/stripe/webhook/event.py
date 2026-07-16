from typing import NamedTuple


class Event(NamedTuple):
    type: str
    data: dict[str, str | None]
