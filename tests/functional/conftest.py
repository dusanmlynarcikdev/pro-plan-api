from collections.abc import AsyncGenerator, Generator
from unittest.mock import patch

from alembic import command
from alembic.config import Config
from alembic.util.exc import CommandError
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy_utils import create_database, database_exists, drop_database
from sqlmodel.ext.asyncio.session import AsyncSession

load_dotenv(".env.dist", override=True)
load_dotenv(".env.test", override=True)

import app.presentation.api.lifespan as lifespan_module
from app.infrastructure.config import get_config
from app.infrastructure.persistence.connection import engine
from app.presentation.api.dependencies import get_session
from app.presentation.api.main import app


@fixture
def client() -> Generator[TestClient]:
    api_token = "test"

    with (
        patch.object(
            lifespan_module, "get_or_create_api_token", return_value=api_token
        ),
        TestClient(app) as client,
    ):
        client.headers["Authorization"] = f"Bearer {api_token}"
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
    database_url = str(get_config().database_url)

    alembic_config = Config("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", database_url)

    if database_exists(database_url):
        try:
            command.check(alembic_config)
            return
        except CommandError:
            drop_database(database_url)

    create_database(database_url)
    command.upgrade(alembic_config, "head")
