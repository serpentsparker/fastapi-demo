import sqlalchemy
from sqlalchemy import orm


class SQLAlchemySessionFactory:
    def __init__(self, engine: sqlalchemy.Engine):
        self._engine = engine
        self._session_maker = orm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def get_session(self) -> orm.Session:
        return orm.scoped_session(self._session_maker)


def create_postgresql_engine(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
) -> sqlalchemy.Engine:
    database_url = rf"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

    return sqlalchemy.create_engine(database_url)
