import dataclasses
import logging
from typing import Any

import pytest
import sqlalchemy
from sqlalchemy import orm

from myapi import database as interfaces
from myapi.actors import database, exceptions, models, service

logger = logging.getLogger(__name__)


class Singleton(type):
    """Metaclass for Singleton."""

    _instances: dict[Any, Any] = {}

    def __call__(cls, *args, **kwargs):
        """Arguments to the '__init__' method do not affect the returned instance."""

        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class TestActorRepository(metaclass=Singleton):
    actor_count = 0
    domain_actors: list[service.Actor] = []

    def create_domain_actor(self) -> service.Actor:
        """Factory method to create Actor domain model instances for testing.

        Returns:
            service.Actor: Instance of the Actor domain model.
        """

        self.actor_count += 1
        logger.info(
            f"Creating an actor domain model instance with ID {self.actor_count}"
        )

        actor = service.Actor(self.actor_count, "Test", "Actor")
        self.domain_actors.append(actor)

        return actor


@pytest.fixture(name="actor_table", scope="module", autouse=True)
def create_actor_table(
    db_engine: sqlalchemy.Engine,
    db_session_factory: interfaces.SQLAlchemySessionFactory,
):
    """Creates the 'actor' table on the test database to be used for tests of this module.

    Args:
        db_engine (sqlalchemy.Engine): SQLAlchemy database engine for the test database.
        db_session_factory (interfaces.SQLAlchemySessionFactory): Factory for SQLAlchemy sessions to
            the engine's database.

    Yields:
        tuple[ list[service.Actor], list[models.Actor] ]: A tuple that contains two elements.
            The first element is a list of actor domain models that were added to the database.
            The second element is a list of actor database models that represent the domain models.
    """

    # Create the actor database table on the test database
    models.Actor.metadata.create_all(db_engine)

    # Create some actor domain model instances for testing
    actor_repository = TestActorRepository()
    domain_actors: list[service.Actor] = []
    for _ in range(5):
        domain_actors.append(actor_repository.create_domain_actor())

    # Create actor database model instances for the domain actors
    db_actors = [
        models.Actor(actor.first_name, actor.last_name) for actor in domain_actors
    ]

    # Add the actors to the actor table on the test database
    db_session = db_session_factory.get_session()
    db_session.add_all(db_actors)
    db_session.commit()

    yield domain_actors, db_actors

    models.Actor.metadata.drop_all(db_engine)


class TestSQLAlchemyActorMapper:
    @pytest.fixture(name="mapper_under_test", scope="class")
    def get_mapper_under_test(
        self, db_session_factory: interfaces.SQLAlchemySessionFactory
    ):
        """Yields a generator of SQLAlchemyActorMapper that can be used by tests of this class.

        Yields:
            Iterator[database.SQLAlchemyActorMapper]: Generates SQLAlchemyActorMapper objects.
        """

        yield database.SQLAlchemyActorMapper(db_session_factory)

    def test_create_actor_return_value(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        actor_repository = TestActorRepository()

        expected_actor = actor_repository.create_domain_actor()
        domain_actor = mapper_under_test.create_actor(
            expected_actor.first_name, expected_actor.last_name
        )

        assert domain_actor == expected_actor

    def test_create_actor_database_record(
        self, mapper_under_test: database.SQLAlchemyActorMapper, db_session: orm.Session
    ):
        actor_repository = TestActorRepository()

        expected_actor = actor_repository.create_domain_actor()
        domain_actor = mapper_under_test.create_actor(
            expected_actor.first_name, expected_actor.last_name
        )

        database_actor = (
            db_session.query(models.Actor)
            .filter(models.Actor.actor_id == domain_actor.actor_id)
            .one()
        )

        database_actor_values = set(dataclasses.astuple(database_actor))
        expected_database_actor_values = set(dataclasses.astuple(domain_actor))

        assert database_actor_values.issuperset(expected_database_actor_values)

    def test_read_actor_return_value(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        actor_repository = TestActorRepository()
        test_actor_id = 3

        expected_actor = actor_repository.domain_actors[test_actor_id - 1]
        domain_actor = mapper_under_test.read_actor(test_actor_id)

        assert domain_actor == expected_actor

    def test_read_missing_actor(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        with pytest.raises(exceptions.ActorNotFoundError):
            mapper_under_test.read_actor(0)

    def test_read_actors_return_value(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        actor_repository = TestActorRepository()

        expected_actors = actor_repository.domain_actors
        actors = mapper_under_test.read_actors()

        assert actors == expected_actors

    def test_update_missing_actor_first_name(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        with pytest.raises(exceptions.ActorNotFoundError):
            mapper_under_test.update_actor_first_name(0, "")

    def test_update_missing_actor_last_name(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        with pytest.raises(exceptions.ActorNotFoundError):
            mapper_under_test.update_actor_last_name(0, "")

    def test_delete_missing_actor(
        self, mapper_under_test: database.SQLAlchemyActorMapper
    ):
        with pytest.raises(exceptions.ActorNotFoundError):
            mapper_under_test.delete_actor(0)
