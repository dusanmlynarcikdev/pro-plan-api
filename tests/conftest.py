from typing import Generator
from pytest import fixture

from fastapi.testclient import TestClient

from app.main import app


@fixture(scope="function")
def client() -> Generator[TestClient]:
    yield TestClient(app)
