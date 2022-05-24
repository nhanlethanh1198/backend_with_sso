"""Add relation store

Revision ID: de80b6d9696b
Revises: 6fce5e85bf84
Create Date: 2022-03-09 23:08:02.277928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de80b6d9696b'
down_revision = '6fce5e85bf84'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stores', sa.Column('staff_id', sa.Integer, sa.ForeignKey('staffs.id')) )


def downgrade():
    pass
