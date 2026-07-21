import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.presentation.api.security import get_or_create_api_token

uvicorn_logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.api_token = api_token = get_or_create_api_token()
    uvicorn_logger.info("API token: %s", api_token)
    yield
