"""update status history in task table

Revision ID: c6d61189f7c8
Revises: 5f6da8f2e0c1
Create Date: 2022-02-03 22:50:31.215737

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision = 'c6d61189f7c8'
down_revision = '5f6da8f2e0c1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('status_history', pg.JSONB(), nullable=True))


def downgrade():
    op.drop_column('tasks', 'status_history')
