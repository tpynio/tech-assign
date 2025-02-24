from app.routers.periodic.schemas.periodic import CachedUSDValue, ForcePeriodicTask
from core.logger import init_logger
from fastapi import APIRouter
from periodic.crud.usd import get_usd_from_redis
from periodic.tasks import update_delivery_price, update_usd_value

log = init_logger(__name__)
router = APIRouter(
    tags=["Periodic"],
)


@router.post(
    "/force_cache_usd_data/",
    response_model=ForcePeriodicTask,
    description="Отладочный ентрипойнт. Форсировать сохранение значения курса доллара к рублю. "
    "По умолчанию, это происходит в отдельном периодическом процессе",
)
async def force_cache_usd_data():
    update_usd_value.apply_async()
    return {"status": "success"}


@router.get(
    "/get_cached_usd_data/",
    response_model=CachedUSDValue,
    description="Отладочный ентрипойнт. Получение сохраненного периодической задачей значения курса доллара к рублю. ",
)
async def get_cached_usd_data():
    usd_value = await get_usd_from_redis()

    return {"value": usd_value}


@router.post(
    "/force_delivery_recalculate/",
    response_model=ForcePeriodicTask,
    description="Отладочный ентрипойнт. Форсированный запуск процесса перерасчета. "
    "По умолчанию, это происходит в отдельном периодическом процессе",
)
async def force_delivery_recalculate():
    update_delivery_price.apply_async()

    return {"status": "success"}
