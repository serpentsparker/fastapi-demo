import dataclasses
import os


@dataclasses.dataclass
class DatabaseConfiguration:
    host: str
    port: int
    user: str
    password: str
    name: str

    @classmethod
    def from_environment(cls):
        try:
            host = os.environ["DATABASE_HOST"]
            port = int(os.environ.get("DATABASE_PORT", "5432"))
            user = os.environ["DATABASE_USER"]
            password = os.environ["DATABASE_PASSWORD"]
            name = os.environ.get("DATABASE_NAME", "myapi")
        except KeyError as exc:
            raise EnvironmentError(f"Missing environment variable '{exc.args[0]}'")

        return cls(host, port, user, password, name)
