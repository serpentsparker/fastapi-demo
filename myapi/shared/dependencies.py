from sqlalchemy import orm

from myapi.shared import configuration
from myapi.shared.database import session

database_configuration = configuration.DatabaseConfiguration.from_environment()
database_engine = session.create_postgresql_engine(
    database_configuration.host,
    database_configuration.port,
    database_configuration.user,
    database_configuration.password,
    database_configuration.name,
)
database_session_factory = session.SQLAlchemySessionFactory(database_engine)


def get_database_session() -> orm.Session:
    return database_session_factory.get_session()
