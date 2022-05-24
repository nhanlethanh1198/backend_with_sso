"""update products table

Revision ID: 91b7becd878c
Revises: 53404876c9cc
Create Date: 2022-02-28 11:26:49.597448

"""
import sqlalchemy as sa
from alembic.op import add_column, drop_column

# revision identifiers, used by Alembic.
revision = '91b7becd878c'
down_revision = '53404876c9cc'
branch_labels = None
depends_on = None


def upgrade():
    add_column('products', sa.Column('is_show_on_combo', sa.Boolean(), nullable=False, server_default='1'))


def downgrade():
    drop_column('products', 'is_show_on_combo')
