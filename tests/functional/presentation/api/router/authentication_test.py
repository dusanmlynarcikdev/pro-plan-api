import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.presentation.api.main import app

PUBLIC_PATHS = {"/api/", "/api/webhooks/stripe"}


request_parameter = pytest.mark.parametrize(
    "method, url",
    [
        (method, path)
        for path, operations in app.openapi()["paths"].items()
        if path not in PUBLIC_PATHS
        for method in operations
    ],
)


@request_parameter
def test_invalid_token(client: TestClient, method: str, url: str) -> None:
    client.headers["Authorization"] = "Bearer invalid_token"

    response = client.request(method, url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Unauthorized"}'


@request_parameter
def test_missing_token(client: TestClient, method: str, url: str) -> None:
    del client.headers["Authorization"]

    response = client.request(method, url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Not authenticated"}'
