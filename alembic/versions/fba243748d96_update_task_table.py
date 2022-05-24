"""update task table

Revision ID: fba243748d96
Revises: eb4c2ff64103
Create Date: 2022-01-17 11:22:57.995617

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fba243748d96'
down_revision = 'eb4c2ff64103'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('tasks', 'start_time')
    op.drop_column('tasks', 'end_time')
    op.add_column('tasks', sa.Column('start_time', sa.DateTime(), nullable=False, server_default='now()'))
    op.add_column('tasks', sa.Column('end_time', sa.DateTime(), nullable=False, server_default='now()'))


def downgrade():
    pass
