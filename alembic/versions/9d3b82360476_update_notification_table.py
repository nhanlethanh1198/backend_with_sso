"""update notification table

Revision ID: 9d3b82360476
Revises: d575a1a2a143
Create Date: 2022-03-18 16:13:10.133938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d3b82360476'
down_revision = 'd575a1a2a143'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('notifications', sa.Column('is_read', sa.Boolean, default=False))


def downgrade():
    pass
