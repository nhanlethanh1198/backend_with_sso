"""update order table

Revision ID: 094d135d794b
Revises: 5cd63deca2ed
Create Date: 2021-11-30 11:06:39.335406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '094d135d794b'
down_revision = '5cd63deca2ed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('note', sa.Text, nullable=True))


def downgrade():
    pass
