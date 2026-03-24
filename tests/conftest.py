from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app


@fixture(scope="function")
def client() -> Generator[TestClient]:
    yield TestClient(app)
