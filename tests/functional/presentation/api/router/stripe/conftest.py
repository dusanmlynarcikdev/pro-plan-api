from collections.abc import Generator
from unittest.mock import Mock, patch

from pytest import fixture

from app.presentation.api import dependencies as dependencies_module
from app.presentation.api.dependencies import get_stripe_client


@fixture(autouse=True)
def _clear_stripe_client_cache() -> Generator[None]:
    yield
    get_stripe_client.cache_clear()


@fixture
def stripe_client() -> Generator[Mock]:
    with patch.object(dependencies_module, "StripeClient") as client:
        yield client
