"""Update store table

Revision ID: d674c11fbba2
Revises: ba6ba7c85cb6
Create Date: 2022-02-08 20:59:46.089135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd674c11fbba2'
down_revision = 'ba6ba7c85cb6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stores', sa.Column('full_address', sa.Unicode(), nullable=True))


def downgrade():
    op.drop_column('stores', 'full_address')
