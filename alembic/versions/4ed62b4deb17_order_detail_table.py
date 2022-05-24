"""order detail table

Revision ID: 4ed62b4deb17
Revises: 26063abbed31
Create Date: 2021-09-25 17:29:11.376050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed62b4deb17'
down_revision = '26063abbed31'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'detail_orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String),
        sa.Column('product_name', sa.String),
        sa.Column('product_image', sa.String),
        sa.Column('original_price', sa.Float),
        sa.Column('sale_price', sa.Float),
        sa.Column('weight', sa.Float),
        sa.Column('unit', sa.String),
        sa.Column('count', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('order_id', sa.Integer),
        sa.ForeignKeyConstraint(('order_id',), ['orders.id'])
    )


def downgrade():
    pass
