"""Update Word table (make english word optional)

Revision ID: 387204e2974c
Revises: c6ec017edca1
Create Date: 2024-06-28 18:09:01.973721

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '387204e2974c'
down_revision: Union[str, None] = 'c6ec017edca1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('word', 'english_word',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('word', 'english_word',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
