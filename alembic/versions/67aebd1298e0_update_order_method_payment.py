"""update order method payment

Revision ID: 67aebd1298e0
Revises: 094d135d794b
Create Date: 2021-11-30 11:48:02.884250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67aebd1298e0'
down_revision = '094d135d794b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('method_payment', sa.String))


def downgrade():
    pass
