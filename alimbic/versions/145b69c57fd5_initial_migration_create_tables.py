"""Initial migration: Create tables

Revision ID: 145b69c57fd5
Revises: 7e03959fbf7d
Create Date: 2024-12-29 16:45:06.448112

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '145b69c57fd5'
down_revision: Union[str, None] = '7e03959fbf7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('item')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('login', sa.VARCHAR(length=50), nullable=True),
    sa.Column('password', sa.VARCHAR(length=50), nullable=True),
    sa.Column('ipn', sa.INTEGER(), nullable=True),
    sa.Column('full_name', sa.VARCHAR(length=150), nullable=True),
    sa.Column('contacts', sa.VARCHAR(length=150), nullable=True),
    sa.Column('photo', sa.VARCHAR(length=150), nullable=True),
    sa.Column('email', sa.VARCHAR(length=150), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('ipn'),
    sa.UniqueConstraint('login')
    )
    op.create_table('item',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('photo', sa.VARCHAR(length=150), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('description', sa.VARCHAR(length=150), nullable=True),
    sa.Column('price_hour', sa.INTEGER(), nullable=True),
    sa.Column('price_day', sa.INTEGER(), nullable=True),
    sa.Column('price_month', sa.INTEGER(), nullable=True),
    sa.Column('price_year', sa.INTEGER(), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###
