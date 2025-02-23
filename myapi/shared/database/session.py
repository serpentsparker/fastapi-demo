import contextlib
from typing import Iterator

import sqlalchemy
from sqlalchemy import orm


class SQLAlchemySessionFactory:
    def __init__(self, host: str, port: int, user: str, password: str, name: str):
        database_url = rf"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"
        self.engine = sqlalchemy.create_engine(
            database_url, poolclass=sqlalchemy.NullPool
        )
        self.sessionmaker = orm.sessionmaker(bind=self.engine, expire_on_commit=False)

    @contextlib.contextmanager
    def get_session(self) -> Iterator[orm.Session]:
        """A generator for SQLAlchemy ORM sessions to the database.

        Yields:
            Iterator[orm.Session]: A SQLAlchemy ORM session to the database.
        """

        with self.sessionmaker.begin() as session:  # pylint: disable=no-member
            yield session
