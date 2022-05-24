"""create order_details

Revision ID: 07abbcf1e8e0
Revises: 27760a0313a0
Create Date: 2022-02-21 13:51:53.430990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07abbcf1e8e0'
down_revision = '27760a0313a0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('order_details',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
                    sa.Column('order_id', sa.Integer, sa.ForeignKey('orders.id')),
                    sa.Column('is_combo', sa.Boolean, server_default='false'),
                    sa.Column('code', sa.String(10), nullable=False),
                    sa.Column('name', sa.String(100), nullable=False),
                    sa.Column('image', sa.String(255), nullable=False),
                    sa.Column('price', sa.Float, nullable=False, server_default='0'),
                    sa.Column('price_sale', sa.Float, nullable=False, server_default='0'),
                    sa.Column('weight', sa.Float, nullable=False, server_default='0'),
                    sa.Column('unit', sa.String(20), nullable=False),
                    sa.Column('quantity', sa.Integer, nullable=False, server_default='1'),
                    sa.Column('created_at', sa.DateTime, nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime, nullable=False, server_default='now()'),
                    )


def downgrade():
    op.drop_table('order_details')
