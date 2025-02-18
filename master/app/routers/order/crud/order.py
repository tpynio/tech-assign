from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import User, Order, OrderType
from core.database.models.order import OrderTypes
from app.routers.order.schemas.order import RegisterOrderParams, Filter
from typing import Sequence
from fastapi_pagination import Page, Params as PaginationParams
from fastapi_pagination.ext.sqlalchemy import paginate
import logging

log = logging.getLogger(__name__)


async def create_order(
    db_session: AsyncSession,
    user: User,
    params: RegisterOrderParams,
) -> Order:
    order_type = await db_session.get(OrderType, OrderTypes.index(params.type) + 1)

    order = Order(
        user=user,
        name=params.name,
        weight=params.weight * 1000,  # перевод в граммы
        price=params.price * 100,  # перевод в центы
        order_type=order_type,
        deliver_id=0,
    )
    db_session.add(order)
    try:
        await db_session.commit()
        await db_session.refresh(order)
    except SQLAlchemyError as exc:
        log.error("Database error", exc_info=exc)

    return order


async def order_types(db_session: AsyncSession) -> Sequence[OrderType]:
    stmt = select(OrderType).order_by(OrderType.id)
    result: Result = await db_session.execute(stmt)
    return result.scalars().all()


async def get_order(
    db_session: AsyncSession,
    user: User,
    order_id: int,
) -> Order | None:
    stmt = select(Order).where(
        Order.id == order_id,
        Order.user_id == user.id,
    )
    result: Result = await db_session.execute(stmt)
    return result.scalar_one_or_none()


async def get_order_list(
    db_session: AsyncSession,
    user: User,
    params: Filter,
) -> Sequence[Order]:
    stmt = (
        select(Order)
        .where(
            Order.user_id == user.id,
            Order.type_id == OrderType.id,
        )
        .order_by(Order.id)
        .offset(params.offset)
        .limit(params.limit)
    )

    result: Result = await db_session.execute(stmt)
    return result.scalars().all()


async def get_order_list_paginate(
    db_session: AsyncSession,
    user: User,
    params: PaginationParams,
) -> Page:
    query = (
        select(Order, OrderType)
        .where(
            Order.user_id == user.id,
            Order.type_id == OrderType.id,
        )
        .with_only_columns(
            Order.id,
            Order.name,
            Order.weight,
            Order.price,
            OrderType.name,
            Order.delivery_price,
            Order.deliver_id,
        )
    )
    return await paginate(db_session, query, params)
