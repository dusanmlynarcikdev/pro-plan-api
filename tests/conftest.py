from typing import AsyncGenerator, Generator

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database, database_exists
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv(".env.test")

from app.infrastructure.database import DATABASE_URL, engine, get_session
from app.main import app


@fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@fixture
async def session() -> AsyncGenerator[AsyncSession]:
    async with engine.connect() as connection:
        transaction = await connection.begin()
        async with AsyncSession(connection, expire_on_commit=False) as session_:
            app.dependency_overrides[get_session] = lambda: session_
            try:
                yield session_
            finally:
                app.dependency_overrides.pop(get_session, None)
        await transaction.rollback()


@fixture(scope="session", autouse=True)
def prepare_database() -> None:
    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)
