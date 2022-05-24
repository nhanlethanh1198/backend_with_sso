"""update product sale count

Revision ID: f162eab512cf
Revises: 6ec44d8477c3
Create Date: 2021-12-28 16:39:40.916449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f162eab512cf'
down_revision = '6ec44d8477c3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('products', sa.Column(
        'sale_count', sa.Integer(), server_default='0', nullable=False))


def downgrade():
    op.drop_column('products', 'sale_count')
