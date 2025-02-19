import asyncio
from core.logger import init_logger
from celery import Celery
from core.config import settings
from periodic.crud.usd import saving_usd_to_redis

log = init_logger(__name__)


app = Celery(
    "tasks",
    broker=f"{settings.REDIS_URL}/0",
)
app.conf.broker_connection_retry_on_startup = True


@app.task
def update_usd_value():
    log.info("Start periodic task check USD completing")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(saving_usd_to_redis())
    log.info("Finished periodic task check USD completing")


@app.task
def update_delivery_price():
    log.info("Periodic task update delivery_price completing")
