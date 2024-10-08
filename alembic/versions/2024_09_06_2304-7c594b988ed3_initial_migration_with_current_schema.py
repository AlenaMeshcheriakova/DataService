"""Initial migration with current schema

Revision ID: 7c594b988ed3
Revises: bd6045c60f94
Create Date: 2024-09-06 23:04:36.669384

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c594b988ed3'
down_revision: Union[str, None] = 'bd6045c60f94'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('lang_level',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('lang_level', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('lang_level')
    )
    op.create_table('user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('auth_user_id', sa.Uuid(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=False),
    sa.Column('training_length', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('auth_user_id'),
    sa.UniqueConstraint('user_name')
    )
    op.create_table('word_type',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('word_type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word_type')
    )
    op.create_table('group',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('group_name', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('group_name', 'user_id', name='uq_group_name_user_id')
    )
    op.create_table('word',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('german_word', sa.String(), nullable=False),
    sa.Column('english_word', sa.String(), nullable=True),
    sa.Column('russian_word', sa.String(), nullable=False),
    sa.Column('lang_level_id', sa.Uuid(), nullable=False),
    sa.Column('word_type_id', sa.Uuid(), nullable=False),
    sa.Column('group_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('amount_already_know', sa.Integer(), nullable=False),
    sa.Column('amount_back_to_learning', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['lang_level_id'], ['lang_level.id'], ondelete='NO ACTION'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_type_id'], ['word_type.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('german_word', 'user_id', name='uq_german_word_user_id')
    )
    op.create_table('standard_word_user',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('word_id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('amount_already_know', sa.Integer(), nullable=False),
    sa.Column('amount_back_to_learning', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['word_id'], ['word.id'], ondelete='NO ACTION'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('word_id', 'user_id', name='uq_word_id_user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('standard_word_user')
    op.drop_table('word')
    op.drop_table('group')
    op.drop_table('word_type')
    op.drop_table('user')
    op.drop_table('lang_level')
    # ### end Alembic commands ###
