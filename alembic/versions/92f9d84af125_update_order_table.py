"""update order table

Revision ID: 92f9d84af125
Revises: c6d61189f7c8
Create Date: 2022-02-04 00:13:20.466486

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = '92f9d84af125'
down_revision = 'c6d61189f7c8'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('order_id', sa.String(length=100), nullable=False, server_default='OD000000'))
    op.add_column('orders', sa.Column('status_history', pg.JSONB(), nullable=True))


def downgrade():
    op.drop_column('orders', 'order_id')
    op.drop_column('orders', 'status_history')
