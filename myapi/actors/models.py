import datetime

import sqlalchemy
from sqlalchemy import orm

from myapi import database


class Actor(database.DataclassBase):
    __tablename__ = "actor"

    actor_id: orm.Mapped[int] = orm.mapped_column(init=False, primary_key=True)
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str] = orm.mapped_column(index=True)
    last_update: orm.Mapped[datetime.datetime] = orm.mapped_column(
        server_default=sqlalchemy.func.now(), default=None
    )
