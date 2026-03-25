from typing import AsyncGenerator, Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database as sqlalchemy_create_database
from sqlalchemy_utils import database_exists as sqlalchemy_database_exists
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.database import create_engine, get_session, get_session_factory
from app.main import app

DATABASE_URL = "postgresql+psycopg://postgres:postgres@database:5432/test"
database_engine = create_engine(DATABASE_URL)


@fixture(scope="function")
def client() -> Generator[TestClient]:
    yield TestClient(app)


@fixture(scope="function", name="session")
async def get_session_override() -> AsyncGenerator[AsyncSession]:
    async with get_session_factory(database_engine) as session:
        yield session


@fixture(scope="session", autouse=True)
def create_database() -> Generator[None]:
    if not sqlalchemy_database_exists(DATABASE_URL):
        sqlalchemy_create_database(DATABASE_URL)

    SQLModel.metadata.create_all(database_engine)
    yield
    SQLModel.metadata.drop_all(database_engine)


@fixture(scope="session", autouse=True)
def override_dependencies() -> Generator[None]:
    app.dependency_overrides[get_session] = get_session_override
    yield
    app.dependency_overrides.clear()
