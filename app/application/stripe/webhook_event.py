from typing import Any, NamedTuple


class WebhookEvent(NamedTuple):
    type: str
    data: dict[str, Any]
