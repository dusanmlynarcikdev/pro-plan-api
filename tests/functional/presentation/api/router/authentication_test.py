from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from tests.functional.presentation.api.router.subscription import (
    create_or_update_test,
    get_test,
    renew_test,
)

request_config_parameter = pytest.mark.parametrize(
    "request_config",
    [
        {
            "url": create_or_update_test.PATH,
            "method": "POST",
            "json": {
                "email": "john@doe.com",
                "period": "yearly",
            },
        },
        {
            "url": get_test.PATH.format(email="john@doe.com"),
            "method": "GET",
        },
        {
            "url": renew_test.PATH.format(email="john@doe.com"),
            "method": "POST",
        },
    ],
)


@request_config_parameter
def test_invalid_api_key(client: TestClient, request_config: dict[str, Any]) -> None:
    client.headers["Authorization"] = "Bearer invalid_api_key"

    response = client.request(**request_config)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Unauthorized"}'


@request_config_parameter
def test_missing_api_key(client: TestClient, request_config: dict[str, Any]) -> None:
    del client.headers["Authorization"]

    response = client.request(**request_config)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Not authenticated"}'
