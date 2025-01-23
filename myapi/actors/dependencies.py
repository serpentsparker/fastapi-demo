from myapi import configuration, database
from myapi.actors import database as actor_database
from myapi.actors import service

database_configuration = configuration.DatabaseConfiguration.from_environment()
database_engine = database.create_postgresql_engine(
    database_configuration.host,
    database_configuration.port,
    database_configuration.user,
    database_configuration.password,
    database_configuration.name,
)
database_session_factory = database.SQLAlchemySessionFactory(database_engine)


def get_actor_mapper() -> service.ActorMapper:
    return actor_database.SQLAlchemyActorMapper(database_session_factory)
