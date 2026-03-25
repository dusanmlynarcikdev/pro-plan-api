from typing import AsyncGenerator, Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database as sqlalchemy_create_database
from sqlalchemy_utils import database_exists as sqlalchemy_database_exists
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.database import create_engine, get_session, get_session_factory
from app.main import app

DATABASE_URL = "postgresql+psycopg://postgres:postgres@database:5432/test"
database_engine = create_engine(DATABASE_URL)


@fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@fixture
async def session() -> AsyncGenerator[AsyncSession]:
    async with get_session_factory(database_engine)() as session_:
        transaction = await session_.begin()
        app.dependency_overrides[get_session] = lambda: session_
        try:
            yield session_
        finally:
            app.dependency_overrides.pop(get_session, None)
            await transaction.rollback()


@fixture(scope="session", autouse=True)
def create_database() -> None:
    if not sqlalchemy_database_exists(DATABASE_URL):
        sqlalchemy_create_database(DATABASE_URL)
