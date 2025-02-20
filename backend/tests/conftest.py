import asyncio
import uuid
from os import getenv
from typing import AsyncGenerator

import pytest
from app.mainRouter import main_router
from core.database.dbHelper import db
from core.database.models.user import User
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from pytest import fixture
from sqlalchemy.ext.asyncio import AsyncSession

if getenv("TESTING") != "1":
    pytest.exit("is not in testing env")

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


@fixture
async def async_session() -> AsyncSession:
    async with db.async_session_maker() as session:
        yield session


@fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@fixture
def auth_user_session_id() -> uuid.UUID:
    return uuid.uuid4()


@fixture
async def auth_user(
    async_session: AsyncSession, auth_user_session_id
) -> AsyncGenerator[User, None]:
    user = User(id=auth_user_session_id.bytes)

    async_session.add(user)
    await async_session.commit()

    yield user

    await async_session.delete(user)
    await async_session.commit()
