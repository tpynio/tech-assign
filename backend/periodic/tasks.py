import asyncio
from core.logger import init_logger
from celery import Celery
from core.config import settings
from periodic.crud.usd import saving_usd_to_redis
from periodic.crud.orderCalculate import order_delivery_calculate

log = init_logger(__name__)


app = Celery(
    "tasks",
    broker=f"{settings.REDIS_URL}/0",
)
app.conf.broker_connection_retry_on_startup = True


@app.task
def update_usd_value():
    log.info("Start periodic task check USD")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(saving_usd_to_redis())
    log.info("Finished periodic task check USD")


@app.task
def update_delivery_price():
    log.info("Start periodic task update delivery_price")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(order_delivery_calculate())
    log.info("Finish periodic task update delivery_price")
