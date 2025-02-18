from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import User, Order, OrderType
from core.database.models.order import OrderTypes
from app.routers.order.schemas.order import RegisterOrderParams
from typing import Sequence


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
    await db_session.commit()

    return order


async def order_types(db_session: AsyncSession) -> Sequence[OrderType]:
    stmt = select(OrderType).order_by(OrderType.id)
    result = await db_session.scalars(stmt)
    return result.all()
