from typing import AsyncGenerator, Generator

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database as sqlalchemy_create_database
from sqlalchemy_utils import database_exists as sqlalchemy_database_exists
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv(".env.test")

from app.infrastructure.database import DATABASE_URL, get_session
from app.main import app


@fixture
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client


@fixture
async def session() -> AsyncGenerator[AsyncSession]:
    async for session_ in get_session():
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
