"""Add user_id to group

Revision ID: 5f922f0cd257
Revises: 07e9b0e9bb9e
Create Date: 2024-07-17 11:41:48.977561

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f922f0cd257'
down_revision: Union[str, None] = '07e9b0e9bb9e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'group', 'user', ['user_id'], ['id'], ondelete='CASCADE')

    op.drop_column('user', 'training_length')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('training_length', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'group', type_='foreignkey')
    op.drop_column('group', 'user_id')
    # ### end Alembic commands ###