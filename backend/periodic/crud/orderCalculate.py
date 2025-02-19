from core.database.dbHelper import db
from core.config import settings
from core.logger import init_logger
from core.database.models.order import Order
from sqlalchemy import select, Result
from sqlalchemy.exc import SQLAlchemyError
from periodic.crud.usd import get_usd_from_redis

log = init_logger(__name__)


async def order_delivery_calculate():
    data_is_here: bool = True
    batch_size = settings.BATCH_SIZE
    value: str | None = await get_usd_from_redis()

    if not value:
        log.info("No USD-data for calculating")
        return

    try:
        usd_value: float = float(value)
    except ValueError as exc:
        log.error("USD-data wrong format %s", value, exc_info=exc)
        return

    while data_is_here:
        query = select(Order).where(Order.delivery_price.is_(None)).limit(batch_size)
        async with db.async_session_maker() as session:
            result: Result = await session.execute(query)
            orders = list(result.scalars().all())
            if len(orders) < batch_size:
                data_is_here = False
            for order in orders:
                # Стоимость = (вес в кг * 0.5 $/кг + стоимость содержимого,$ * 0.01 ) * курс доллара к рублю, р/$
                # в бд : вес в граммах, а денежные значения в центах и копейках, поэтому
                # Стоимость = (вec,г * 0,5 + цена, центы * 0,1) / 10 * курс долар/рубл
                order.delivery_price = int(
                    (order.weight * 0.5 + order.price * 0.1) * usd_value / 10
                )

            try:
                await session.commit()
            except SQLAlchemyError as exc:
                log.error("Error recalculating, continue..", exc_info=exc)
                continue
