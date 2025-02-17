import logging
import uvicorn

from app.main_router import main_router
from core.config import settings

__all__ = (
    "main_router",
    "main",
)


def main():
    uvicorn.run(
        "main:main_router",
        log_level=logging.getLevelName(settings.LOG_LEVEL),
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    main()
