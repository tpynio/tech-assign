from celery import Celery
from core.config import settings
from core.logger import init_logger
from periodic.tasks import update_usd_value

log = init_logger(__name__)

app = Celery(
    "tasks",
    broker=f"{settings.REDIS_URL}/0",
)

app.conf.beat_schedule = {
    "run-every-6h": {
        "task": "periodic.tasks.update_usd_value",
        "schedule": 21600,
    },
    "run-every-5m": {
        "task": "periodic.tasks.update_delivery_price",
        "schedule": 300,
    },
}


@app.on_after_configure.connect
def initial_update_usd_value(**kwargs):
    """
    Запуск сверки курса доллара на старте приложения
    :param kwargs:
    :return:
    """
    update_usd_value.apply_async()
