"""update user table

Revision ID: 1aaa031f3f0e
Revises: 1624c850d7c0
Create Date: 2022-01-31 23:14:53.162259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aaa031f3f0e'
down_revision = '1624c850d7c0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('accumulated_points', sa.Integer, nullable=False, server_default='0'))


def downgrade():
    op.drop_column('users', 'accumulated_points')
