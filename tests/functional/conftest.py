from typing import AsyncGenerator, Generator

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv(".env.test")

from app.infrastructure.persistence.connection import DATABASE_URL, engine
from app.main import app
from app.presentation.api.dependencies import get_session


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
    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", DATABASE_URL)

    if database_exists(DATABASE_URL):
        try:
            command.check(alembic_config)
            return
        except CommandError:
            drop_database(DATABASE_URL)

    create_database(DATABASE_URL)
    command.upgrade(alembic_config, "head")
