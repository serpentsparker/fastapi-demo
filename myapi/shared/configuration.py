import dataclasses
import os


@dataclasses.dataclass
class DatabaseConfiguration:
    def __init__(
        self, host: str, port: int, user: str, password: str, name: str
    ) -> None:
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.name = name

    @classmethod
    def from_environment(cls):
        host = os.environ["DATABASE_HOST"]
        port = int(os.environ["DATABASE_PORT"])
        user = os.environ["DATABASE_USER"]
        password = os.environ["DATABASE_PASSWORD"]
        name = os.environ["DATABASE_NAME"]

        return cls(host, port, user, password, name)
