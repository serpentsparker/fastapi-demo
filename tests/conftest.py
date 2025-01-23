"""Test fixtures and general setup functions for the pytest session."""

from __future__ import annotations

import logging
import pathlib

import pytest
import sqlalchemy

from myapi import database

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def pytest_addoption(parser: pytest.Parser):
    parser.addoption(
        "--database-url",
        action="store",
        default="sqlite:///pytest.db",
        help="URL of the database used for tests by pytest",
    )


@pytest.fixture(scope="session")
def db_engine(request: pytest.FixtureRequest):
    """Yields an instance of a SQLAlchemy database engine and disposes it after the test session.

    Args:
        request (pytest.FixtureRequest): Pytest request object that gives access to the requesting
            test context to obtain values from additional command line options.

    Yields:
        sqlalchemy.Engine: SQLAlchemy database engine for the test database.
    """

    db_url = request.config.getoption("--database-url")

    if "sqlite" in db_url:
        database_file_path = pathlib.Path(db_url[10:]).resolve()
        logger.warning(
            f"The tests are run against an in-memory database at {database_file_path}"
        )

    engine = sqlalchemy.create_engine(db_url, echo=True)

    yield engine

    engine.dispose()

    if "sqlite" in db_url:
        database_file_path.unlink()
        logger.info(
            "Successfully removed the in-memory database that was used for testing"
        )


@pytest.fixture(scope="session")
def db_session_factory(
    db_engine: sqlalchemy.Engine,
) -> database.SQLAlchemySessionFactory:
    """Returns an instance of a SQLAlchemySessionFactory for the given database engine.

    Args:
        db_engine (sqlalchemy.Engine): SQLAlchemy engine to be used by the session factory.

    Returns:
        database.SQLAlchemySessionFactory: Factory for SQLAlchemy sessions to the engine's database.
    """

    return database.SQLAlchemySessionFactory(db_engine)


@pytest.fixture(scope="function")
def db_session(db_session_factory: database.SQLAlchemySessionFactory):
    """Yields a generator for scoped SQLAlchemy sessions to the test database.

    Args:
        db_session_factory (database.SQLAlchemySessionFactory): Factory class for SQLAlchemy
            sessions to the test database

    Yields:
        Iterator[orm.Session]: Generator of SQLAlchemy database sessions for the test database.
    """

    db_session = db_session_factory.get_session()

    yield db_session

    db_session.rollback()
    db_session.close()
