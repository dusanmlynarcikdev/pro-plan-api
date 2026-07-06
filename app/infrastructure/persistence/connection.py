from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.settings import get_settings

engine = create_async_engine(str(get_settings().database_url))
session_factory = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
