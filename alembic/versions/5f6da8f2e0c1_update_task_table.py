"""update task table

Revision ID: 5f6da8f2e0c1
Revises: 1aaa031f3f0e
Create Date: 2022-02-03 21:32:04.034330

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f6da8f2e0c1'
down_revision = '1aaa031f3f0e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('task_id', sa.String(length=100), nullable=False, server_default='T'))


def downgrade():
    op.drop_column('tasks', 'task_id')
