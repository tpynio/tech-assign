import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from core.config import settings
from typing import AsyncGenerator


log = logging.getLogger(__name__)


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        max_overflow: int = 15,
        pool_size: int = 5,
    ):
        log.info("Connecting to %s", url)
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
    url=settings.MYSQL_ADDR,
    echo=settings.ECHO,
    echo_pool=settings.ECHO,
    max_overflow=settings.MAX_OVERFLOW,
    pool_size=settings.POOL_SIZE,
)
