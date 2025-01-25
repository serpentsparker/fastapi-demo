import sqlalchemy
from sqlalchemy import orm


class SQLAlchemySessionFactory:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        database_url = (
            rf"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
        )
        self._engine = sqlalchemy.create_engine(database_url)
        self._session_maker = orm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    def get_session(self) -> orm.Session:
        return orm.scoped_session(self._session_maker)
