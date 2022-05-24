"""update task table

Revision ID: 0e57d069d96e
Revises: 4c5161a2825b
Create Date: 2022-01-18 12:34:17.346508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0e57d069d96e'
down_revision = '4c5161a2825b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('packaging', sa.String(length=30), nullable=True))
    op.add_column('tasks', sa.Column('start_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('end_date', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('schedule', postgresql.ARRAY(sa.DateTime()), nullable=True))


def downgrade():
    op.drop_column('tasks', 'packaging')
    op.drop_column('tasks', 'start_date')
    op.drop_column('tasks', 'end_date')
    op.drop_column('tasks', 'schedule')
