from myapi import database
from myapi.actors import exceptions, models, service


class SQLAlchemyActorMapper(service.ActorMapper):
    def __init__(
        self, database_session_factory: database.SQLAlchemySessionFactory
    ) -> None:
        self._database = database_session_factory

    def create_actor(self, first_name: str, last_name: str) -> service.Actor:
        """Creates a new actor in the database and returns its primary key.

        Args:
            first_name (str): First name of the actor to be created.
            last_name (str): Last name of the actor to be created.

        Returns:
            actor.Actor: Instance of the created actor.
        """

        db_actor = models.Actor(first_name, last_name)

        with self._database.get_session() as db:
            db.add(db_actor)
            db.commit()
            db.refresh(db_actor)

        return service.Actor(
            actor_id=db_actor.actor_id,
            first_name=db_actor.first_name,
            last_name=db_actor.last_name,
        )

    def read_actors(self) -> list[service.Actor]:
        """Returns all actors from the database in a list.

        Returns:
            list[actor.Actor]: List of actor instances.
        """

        with self._database.get_session() as db:
            db_actors = db.query(models.Actor).all()

        return [
            service.Actor(
                actor_id=db_actor.actor_id,
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

        with self._database.get_session() as db:
            db_actor = db.get(models.Actor, actor_id)

            if not db_actor:
                raise exceptions.ActorNotFoundError(actor_id)

        return service.Actor(
            actor_id=db_actor.actor_id,
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

        with self._database.get_session() as db:
            db_actor = db.get(models.Actor, actor_id)

            if not db_actor:
                raise exceptions.ActorNotFoundError(actor_id)

            db_actor.first_name = first_name
            db.commit()
            db.refresh(db_actor)

        return service.Actor(
            actor_id=db_actor.actor_id,
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

        with self._database.get_session() as db:
            db_actor = db.get(models.Actor, actor_id)

            if not db_actor:
                raise exceptions.ActorNotFoundError(actor_id)

            db_actor.last_name = last_name
            db.commit()
            db.refresh(db_actor)

        return service.Actor(
            actor_id=db_actor.actor_id,
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

        with self._database.get_session() as db:
            db_actor = db.get(models.Actor, actor_id)

            if not db_actor:
                raise exceptions.ActorNotFoundError(actor_id)

            db.delete(db_actor)
            db.commit()
