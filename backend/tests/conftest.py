from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from pytest import fixture
from app.mainRouter import main_router
import asyncio
import pytest

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@fixture
def client():
    client = TestClient(main_router)
    return client


@fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(
        transport=ASGITransport(app=main_router), base_url="http://test-backend"
    ) as ac:
        yield ac


@fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()
