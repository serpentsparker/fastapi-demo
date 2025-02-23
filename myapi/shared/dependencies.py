import dataclasses
from typing import Iterator, AsyncIterator

from sqlalchemy import orm
from sqlalchemy.ext import asyncio

from myapi.shared import configuration
from myapi.shared.database import session, async_session

database_configuration = configuration.DatabaseConfiguration.from_environment()
database_session_factory = session.SQLAlchemySessionFactory(
    **dataclasses.asdict(database_configuration)
)
async_database_session_factory = async_session.SQLAlchemyAsyncSessionFactory(
    **dataclasses.asdict(database_configuration)
)


def get_database_session() -> Iterator[orm.Session]:
    """A generator for SQLAlchemy ORM sessions to the database.

    Yields:
        Iterator[orm.Session]: A SQLAlchemy ORM session to the database.
    """

    with database_session_factory.get_session() as database_session:
        yield database_session


async def get_async_database_session() -> AsyncIterator[asyncio.AsyncSession]:
    """A generator for asynchronous SQLAlchemy ORM sessions to the database.

    Yields:
        AsyncIterator[asyncio.AsyncSession]: An asynchronous SQLAlchemy ORM session to the database.
    """

    async with async_database_session_factory.get_session() as async_session:
        yield async_session
