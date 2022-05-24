"""update product table

Revision ID: 53404876c9cc
Revises: 8b02cbfa6b8c
Create Date: 2022-02-27 22:31:11.699042

"""
import sqlalchemy as sa
from alembic.op import add_column, drop_column

# revision identifiers, used by Alembic.
revision = '53404876c9cc'
down_revision = '8b02cbfa6b8c'
branch_labels = None
depends_on = None


def upgrade():
    add_column('products', sa.Column('is_show_on_homepage', sa.Boolean(), nullable=True, server_default='1'))
    add_column('products', sa.Column('is_show_on_store', sa.Boolean(), nullable=True, server_default='1'))


def downgrade():
    drop_column('products', 'is_show_on_homepage')
    drop_column('products', 'is_show_on_store')
