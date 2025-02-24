import asyncio
import uuid
from os import getenv
from typing import AsyncGenerator

import pytest
from app.main_router import main_router
from core.database.db_helper import db
from core.database.models.order import Order, OrderType, OrderTypes
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


@fixture
async def order_dummies_factory(auth_user, async_session):
    class Factory:
        orders = []

        async def make_dummies(
            self,
            name: str,
            price: int,
            weight: int,
            delivery_price: int | None,
            order_type: OrderTypes,
            delivery_id: int = None,
        ):
            order_type = await async_session.get(
                OrderType, OrderTypes.index(order_type) + 1
            )
            order = Order(
                name=name,
                price=price,
                weight=weight,
                order_type=order_type,
                user=auth_user,
                delivery_price=delivery_price,
                deliver_id=delivery_id,
            )
            async_session.add(order)
            await async_session.commit()
            self.orders.append(order)

            return order

        async def destroy_dummies(self):
            for order in self.orders:
                await async_session.delete(order)
            await async_session.commit()

    factory = Factory()
    yield factory
    await factory.destroy_dummies()
