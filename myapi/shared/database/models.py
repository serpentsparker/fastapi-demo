import sqlalchemy
from sqlalchemy import orm, types

POSTGRES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class DataclassBase(orm.MappedAsDataclass, orm.DeclarativeBase):
    metadata = sqlalchemy.MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)


class Actor(DataclassBase):
    __tablename__ = "actor"

    id: orm.MappedColumn[int] = orm.mapped_column(
        types.INTEGER, primary_key=True, init=False
    )
    first_name: orm.MappedColumn[str] = orm.mapped_column(types.TEXT)
    last_name: orm.MappedColumn[str] = orm.mapped_column(types.TEXT)
