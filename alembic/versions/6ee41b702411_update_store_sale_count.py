"""update_store_sale_count

Revision ID: 6ee41b702411
Revises: cba037323fd3
Create Date: 2022-01-03 21:50:44.209721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ee41b702411'
down_revision = 'cba037323fd3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stores', sa.Column('product_sale_count', sa.Integer(), nullable=True, server_default='0'))


def downgrade():
    op.drop_column('stores', 'product_sale_count')
