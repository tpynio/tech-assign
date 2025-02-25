import asyncio
from time import time

from celery import Celery, signals
from core.config import settings
from core.logger import init_logger
from periodic.crud.order_calculate import order_delivery_calculate
from periodic.crud.usd import saving_usd_to_redis

log = init_logger(__name__)


app = Celery(
    "tasks",
    broker=f"{settings.REDIS_URL}/0",
)
app.conf.broker_connection_retry_on_startup = True


@app.task
def update_usd_value():
    log.info("Start periodic task check USD")
    start = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(saving_usd_to_redis())
    log.info("Finished periodic task check USD. elapsed (%f) sec", time() - start)


@app.task
def update_delivery_price():
    log.info("Start periodic task update delivery_price")
    start = time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(order_delivery_calculate())
    log.info(
        "Finish periodic task update delivery_price. elapsed (%f) sec", time() - start
    )


@signals.setup_logging.connect()
def setup_logging(*args, **kwargs):
    pass
