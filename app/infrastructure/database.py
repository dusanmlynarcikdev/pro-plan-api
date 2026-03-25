from functools import cache
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "postgresql+psycopg://postgres:postgres@database:5432/postgres"


@cache
def create_engine(database_url: str) -> AsyncEngine:
    return create_async_engine(database_url)


@cache
def get_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with get_session_factory(create_engine(DATABASE_URL))() as session:
        yield session
