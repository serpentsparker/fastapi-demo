class ActorNotFoundError(Exception):
    """Raised if no actor exists for the given ID.

    Args:
        actor_id (int): Primary key of the actor to be selected.
    """

    def __init__(self, actor_id: int) -> None:
        self.actor_id = actor_id

        super().__init__(f"Actor with ID '{self.actor_id}' does not exist")
