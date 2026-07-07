from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.config import get_config

engine = create_async_engine(str(get_config().database_url))
session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
