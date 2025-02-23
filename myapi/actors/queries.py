from sqlalchemy import orm

from myapi.actors import exceptions, service
from myapi.shared.database import models


class SQLAlchemyActorMapper(service.ActorMapper):
    def __init__(self, database_session: orm.Session) -> None:
        self._db = database_session

    def create_actor(self, first_name: str, last_name: str) -> service.Actor:
        """Creates a new actor in the database and returns its primary key.

        Args:
            first_name (str): First name of the actor to be created.
            last_name (str): Last name of the actor to be created.

        Returns:
            actor.Actor: Instance of the created actor.
        """

        db_actor = models.Actor(first_name=first_name, last_name=last_name)

        self._db.add(db_actor)
        self._db.flush()

        return service.Actor(
            actor_id=db_actor.id,
            first_name=db_actor.first_name,
            last_name=db_actor.last_name,
        )

    def read_actors(self) -> list[service.Actor]:
        """Returns all actors from the database in a list.

        Returns:
            list[actor.Actor]: List of actor instances.
        """

        db_actors = self._db.query(models.Actor).all()

        return [
            service.Actor(
                actor_id=db_actor.id,
                first_name=db_actor.first_name,
                last_name=db_actor.last_name,
            )
            for db_actor in db_actors
        ]

    def read_actor(self, actor_id: int) -> service.Actor:
        """Returns the actor with the given primary key.

        Args:
            actor_id (int): Primary key of the actor to be selected.

        Raises:
            ActorNotFoundError: Raised if no actor exists for the given actor ID.

        Returns:
            actor.Actor: Instance of the actor that matches the given ID.
        """

        db_actor = self._db.get(models.Actor, actor_id)

        if not db_actor:
            raise exceptions.ActorNotFoundError(actor_id)

        return service.Actor(
            actor_id=db_actor.id,
            first_name=db_actor.first_name,
            last_name=db_actor.last_name,
        )

    def update_actor_first_name(self, actor_id: int, first_name: str) -> service.Actor:
        """Updates the first name of a particular actor and returns it.

        Args:
            actor_id (int): Primary key of the actor to be updated.
            first_name (str): Value of the first name to be set.

        Raises:
            ActorNotFoundError: Raised if no actor exists for the given actor ID.

        Returns:
            actor.Actor: Instance of the updated actor.
        """

        db_actor = self._db.get(models.Actor, actor_id)

        if not db_actor:
            raise exceptions.ActorNotFoundError(actor_id)

        db_actor.first_name = first_name
        self._db.flush()

        return service.Actor(
            actor_id=db_actor.id,
            first_name=db_actor.first_name,
            last_name=db_actor.last_name,
        )

    def update_actor_last_name(self, actor_id: int, last_name: str) -> service.Actor:
        """Updates the last name of a particular actor and returns it.

        Args:
            actor_id (int): Primary key of the actor to be updated.
            last_name (str): Value of the last name to be set.

        Raises:
            ActorNotFoundError: Raised if no actor exists for the given actor ID.

        Returns:
            actor.Actor: Instance of the updated actor.
        """

        db_actor = self._db.get(models.Actor, actor_id)

        if not db_actor:
            raise exceptions.ActorNotFoundError(actor_id)

        db_actor.last_name = last_name
        self._db.flush()

        return service.Actor(
            actor_id=db_actor.id,
            first_name=db_actor.first_name,
            last_name=db_actor.last_name,
        )

    def delete_actor(self, actor_id: int) -> None:
        """Deletes a particular actor from the database.

        Args:
            actor_id (int): Primary key of the actor to be deleted.

        Raises:
            ActorNotFoundError: Raised if no actor exists for the given actor ID.
        """

        db_actor = self._db.get(models.Actor, actor_id)

        if not db_actor:
            raise exceptions.ActorNotFoundError(actor_id)

        self._db.delete(db_actor)
