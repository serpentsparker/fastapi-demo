import contextlib
import logging
from typing import AsyncIterator

from sqlalchemy.ext import asyncio

logger = logging.getLogger(__name__)


class SQLAlchemyAsyncSessionFactory:
    def __init__(self, host: str, port: int, user: str, password: str, name: str):
        database_url = rf"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
        self.engine = asyncio.create_async_engine(
            database_url, pool_size=50, max_overflow=0
        )
        self.sessionmaker = asyncio.async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def get_session(self) -> AsyncIterator[asyncio.AsyncSession]:
        """A generator for asynchronous SQLAlchemy ORM sessions to the database.

        Yields:
            AsyncIterator[asyncio.AsyncSession]: An asynchronous SQLAlchemy ORM session to the database.
        """

        async with self.sessionmaker.begin() as session:  # pylint: disable=no-member
            try:
                logger.debug("opened the asynchronous database session.")
                yield session
            finally:
                logger.debug("closed the asynchronous database session.")
