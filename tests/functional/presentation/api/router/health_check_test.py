from fastapi import status
from fastapi.testclient import TestClient


def test_success(client: TestClient) -> None:
    response = client.get("/api")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""
