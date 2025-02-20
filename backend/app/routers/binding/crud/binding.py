import asyncio

from core.database import Order
from core.logger import init_logger
from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

lock = asyncio.Lock()
log = init_logger(__name__)


async def binding_free_order(
    db_session: AsyncSession,
    delivery_id: int,
) -> Order:
    async with lock:
        stmt = select(Order).where(Order.deliver_id.is_(None)).limit(1)
        result: Result = await db_session.execute(stmt)

        order = result.scalar_one_or_none()
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no any free orders",
            )
        order.deliver_id = delivery_id
        await db_session.commit()
        await db_session.refresh(order)
        return order
