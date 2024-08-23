"""Add table progress for detecting user learning 

Revision ID: 119c7ab00123
Revises: 3fcf2819beca
Create Date: 2024-06-25 13:56:29.164309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '119c7ab00123'
down_revision: Union[str, None] = '3fcf2819beca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('progress',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('word_id', sa.Uuid(), nullable=False),
    sa.Column('amount_already_know', sa.Integer(), nullable=False),
    sa.Column('amount_back_to_learning', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('progress')
    # ### end Alembic commands ###