from typing import Any, NamedTuple


class Event(NamedTuple):
    type: str
    data: dict[str, Any]
