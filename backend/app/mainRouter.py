from contextlib import asynccontextmanager

from app import __version__
from app.routers.order.api.order import router as order_router
from app.routers.periodic.api.periodic import router as periodic_router
from app.routers.service.schemas.service import PingResponse
from core.config import settings
from core.database.dbHelper import db
from core.logger import init_logger
from fastapi import FastAPI
from fastapi.responses import UJSONResponse

log = init_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db.dispose()


main_router = FastAPI(
    title=settings.TITLE,
    version=__version__,
    openapi_url=f"{settings.OPENAPI_PREFIX}/openapi.json",
    root_path=settings.ROOT_PATH,
    default_response_class=UJSONResponse,
    lifespan=lifespan,
)


@main_router.get(
    "/ping/",
    tags=["Service"],
    response_model=PingResponse,
    description="Служебный ентрипойнт. Может пригодиться для проверки здоровья приложения(запущено/нет)",
)
async def ping():
    return {"message": "pong"}


main_router.include_router(
    order_router,
    prefix="/api/order",
)

main_router.include_router(
    periodic_router,
    prefix="/api/periodic",
)
