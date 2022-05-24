"""create order table

Revision ID: 26063abbed31
Revises: 19307d2e6079
Create Date: 2021-08-27 18:43:08.151444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26063abbed31'
down_revision = '19307d2e6079'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('fullname', sa.String),
        sa.Column('phone', sa.String),
        sa.Column('address_delivery', sa.String),
        sa.Column('count_product', sa.Integer),
        sa.Column('order_type', sa.String, nullable=True, default=None),
        sa.Column('shipper', sa.String, nullable=True, default=None),
        sa.Column('start_delivery', sa.DateTime, nullable=True, default=None),
        sa.Column('end_delivery', sa.DateTime, nullable=True, default=None),
        sa.Column('voucher', sa.String, nullable=True, default=None),
        sa.Column('total_money', sa.Float),
        sa.Column('total_money_sale', sa.Float),
        sa.Column('product_money', sa.Float),
        sa.Column('ship_fee', sa.Float),
        sa.Column('status', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
