"""Remove description from group

Revision ID: 22e2d022fe41
Revises: d7e67c660def
Create Date: 2024-06-10 15:32:41.509876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22e2d022fe41'
down_revision: Union[str, None] = 'd7e67c660def'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
