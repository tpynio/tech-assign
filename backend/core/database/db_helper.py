from typing import AsyncGenerator

from core.config import settings
from core.logger import init_logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

log = init_logger(__name__)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 15,
        pool_size: int = 5,
    ):
        self.url = url
        log.info("Connecting to %s", self.url)

        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine, expire_on_commit=False
        )

    async def dispose(self):
        await self.engine.dispose()
        log.info("Database connections is closes")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session_maker() as session:
            yield session
            await session.close()


db = DatabaseHelper(
    url=settings.MYSQL_URL,
    echo=settings.ECHO,
    echo_pool=settings.ECHO,
    max_overflow=settings.MAX_OVERFLOW,
    pool_size=settings.POOL_SIZE,
)
