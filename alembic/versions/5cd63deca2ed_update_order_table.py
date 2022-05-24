"""update order table

Revision ID: 5cd63deca2ed
Revises: 2f8d86708a97
Create Date: 2021-11-29 18:37:38.575395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cd63deca2ed'
down_revision = '2f8d86708a97'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('user_id', sa.Integer))


def downgrade():
    pass
