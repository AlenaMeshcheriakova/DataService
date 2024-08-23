"""Add UniqueConstraint(group name and user_id) to group

Revision ID: 28ee946e5e3b
Revises: a025d58798bc
Create Date: 2024-07-19 08:47:48.716228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28ee946e5e3b'
down_revision: Union[str, None] = 'a025d58798bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('uq_group_name_user_id', 'group', ['group_name', 'user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('uq_group_name_user_id', 'group', type_='unique')
    # ### end Alembic commands ###
