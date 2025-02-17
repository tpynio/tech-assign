import logging
import uvicorn

from app.main_router import app
from core.config import settings

__all__ = (
    "app",
    "main",
)


def main():
    uvicorn.run(
        "main:app",
        log_level=logging.getLevelName(settings.LOG_LEVEL),
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )


if __name__ == "__main__":
    main()
