import pytest
from fastapi import status
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

from app.presentation.api.main import app

PUBLIC_PATHS = {"/api/"}


request_parameter = pytest.mark.parametrize(
    "method, url",
    [
        (method, route.path)
        for route in app.routes
        if isinstance(route, APIRoute) and route.path not in PUBLIC_PATHS
        for method in route.methods
    ],
)


@request_parameter
def test_invalid_api_key(client: TestClient, method: str, url: str) -> None:
    client.headers["Authorization"] = "Bearer invalid_api_key"

    response = client.request(method, url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Unauthorized"}'


@request_parameter
def test_missing_api_key(client: TestClient, method: str, url: str) -> None:
    del client.headers["Authorization"]

    response = client.request(method, url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.content == b'{"detail":"Not authenticated"}'
