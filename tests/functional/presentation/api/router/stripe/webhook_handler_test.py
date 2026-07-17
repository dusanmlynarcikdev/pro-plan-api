import hashlib
import hmac
import json
import time
from unittest.mock import patch

import pytest
from fastapi import BackgroundTasks, status
from fastapi.testclient import TestClient

from app.application.stripe.webhook.event import Event
from app.application.stripe.webhook.handle_event_use_case import HandleEventUseCase
from app.infrastructure.config import get_config

PATH = "/api/stripe/webhooks"
PAYLOAD = json.dumps(
    {
        "object": "event",
        "type": "event_type",
        "data": {"object": {"key": "value"}},
    }
).encode()


def test_success(client: TestClient) -> None:
    with patch.object(BackgroundTasks, "add_task") as add_task:
        response = client.post(
            PATH,
            content=PAYLOAD,
            headers={"stripe-signature": _create_signature(PAYLOAD)},
        )

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.content == b"null"

    handler, event = add_task.call_args.args
    assert isinstance(handler, HandleEventUseCase)
    assert event == Event(type="event_type", data={"key": "value"})


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"stripe-signature": "invalid"},
    ],
)
def test_invalid_signature(client: TestClient, headers: dict[str, str]) -> None:
    response = client.post(PATH, content=PAYLOAD, headers=headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.content == b'{"detail":"Invalid webhook"}'


def _create_signature(payload: bytes) -> str:
    timestamp = int(time.time())
    signature = hmac.new(
        get_config().stripe_webhook_secret.encode(),
        f"{timestamp}.".encode() + payload,
        hashlib.sha256,
    ).hexdigest()

    return f"t={timestamp},v1={signature}"
