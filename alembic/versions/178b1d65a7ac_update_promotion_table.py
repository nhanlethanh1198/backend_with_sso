"""update promotion table

Revision ID: 178b1d65a7ac
Revises: a8f21bbfccad
Create Date: 2021-11-28 11:01:10.551815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '178b1d65a7ac'
down_revision = 'a8f21bbfccad'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('promotions', sa.Column('promotion_type',
                  sa.String(length=50), nullable=False))


def downgrade():
    pass
