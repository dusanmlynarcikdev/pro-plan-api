from functools import cache
from os import getenv
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = getenv("DATABASE_URL", "")

engine = create_async_engine(DATABASE_URL)


@cache
def get_session_factory(
    conn: AsyncConnection | AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with get_session_factory(engine)() as session:
        yield session
        await session.commit()
