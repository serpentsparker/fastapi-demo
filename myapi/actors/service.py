import abc
import dataclasses


@dataclasses.dataclass
class Actor:
    actor_id: int
    first_name: str
    last_name: str


class ActorMapper(abc.ABC):
    """Interface for mapper classes related to the Actor domain entity.

    This abstract base class acts as an interface for classes that implement
    data mappers for the Actor domain entity. Their responsibility is to query
    data from the database and directly map it to the Actor domain entity.
    """

    @abc.abstractmethod
    def create_actor(self, first_name: str, last_name: str) -> Actor:
        """Template method to create a new actor in the database."""

    @abc.abstractmethod
    def read_actors(self) -> list[Actor]:
        """Template method to read all actors from the database."""

    @abc.abstractmethod
    def read_actor(self, actor_id: int) -> Actor:
        """Template method to read a particular actor by its primary key."""

    @abc.abstractmethod
    def update_actor_first_name(self, actor_id: int, first_name: str) -> Actor:
        """Template method to update the first name of a particular actor."""

    @abc.abstractmethod
    def update_actor_last_name(self, actor_id: int, last_name: str) -> Actor:
        """Template method to update the last name of a particular actor."""

    @abc.abstractmethod
    def delete_actor(self, actor_id: int) -> None:
        """Template method to delete a particular actor from the database."""
