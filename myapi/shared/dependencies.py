from typing import Iterator

from sqlalchemy import orm

from myapi.shared import configuration
from myapi.shared.database import session

database_configuration = configuration.DatabaseConfiguration.from_environment()
database_session_factory = session.SQLAlchemySessionFactory(
    database_configuration.host,
    database_configuration.port,
    database_configuration.user,
    database_configuration.password,
    database_configuration.name,
)


def get_database_session() -> Iterator[orm.Session]:
    """A generator for SQLAlchemy ORM sessions to the database.

    Yields:
        Iterator[orm.Session]: A SQLAlchemy ORM session to the database.
    """

    with database_session_factory.get_session() as database_session:
        yield database_session
