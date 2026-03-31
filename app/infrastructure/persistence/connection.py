from os import getenv

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = getenv("DATABASE_URL", "")

engine = create_async_engine(DATABASE_URL)
session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
