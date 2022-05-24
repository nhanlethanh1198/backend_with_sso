"""update order table with accumulated_point

Revision ID: f058243ad36f
Revises: 92f9d84af125
Create Date: 2022-02-07 18:56:48.844259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f058243ad36f'
down_revision = '92f9d84af125'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('accumulated_point', sa.Integer(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column('orders', 'accumulated_point')
