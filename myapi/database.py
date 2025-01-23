import sqlalchemy
from sqlalchemy import orm

POSTGRES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

SAKILA_NAMING_CONVENTION = {
    "ix": "idx_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class DataclassBase(orm.MappedAsDataclass, orm.DeclarativeBase):
    metadata = sqlalchemy.MetaData(naming_convention=SAKILA_NAMING_CONVENTION)


class SQLAlchemySessionFactory:
    def __init__(self, engine: sqlalchemy.Engine):
        self._engine = engine
        self._session_maker = orm.sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    # TODO: Use scoped_session https://docs.sqlalchemy.org/en/20/orm/contextual.html
    def get_session(self) -> orm.Session:
        return self._session_maker()


def create_postgresql_engine(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
) -> sqlalchemy.Engine:
    database_url = rf"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"

    return sqlalchemy.create_engine(database_url)
