"""create actor table

Revision ID: 2fc5672004b8
Revises:
Create Date: 2025-01-25 14:33:28.446375

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2fc5672004b8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "actor",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("first_name", sa.TEXT(), nullable=False),
        sa.Column("last_name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("actor_pkey")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("actor")
    # ### end Alembic commands ###
