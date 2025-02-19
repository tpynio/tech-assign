import uvicorn
from app.mainRouter import main_router
from core.logger import init_logger
from core.config import settings


__all__ = (
    "main_router",
    "main",
)

log = init_logger(__name__)


def main():
    log.info("Listen http://%s:%d", settings.HOST, settings.PORT)

    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = log.handlers[0].formatter._fmt
    log_config["formatters"]["access"]["datefmt"] = log.handlers[0].formatter.datefmt
    log_config["formatters"]["default"]["fmt"] = log.handlers[0].formatter._fmt
    log_config["formatters"]["default"]["datefmt"] = log.handlers[0].formatter.datefmt
    uvicorn.run(
        "main:main_router",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_config=log_config,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye!")
