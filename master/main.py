import uvicorn
import logging
from app.main_router import main_router
from core.logger import configure_logging
from core.config import settings


__all__ = (
    "main_router",
    "main",
)

log = logging.getLogger(__name__)
configure_logging()


def main():
    uvicorn.run(
        "main:main_router",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_config=None,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye!")
