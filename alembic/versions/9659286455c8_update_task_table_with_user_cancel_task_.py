"""update task table with user cancel task reasion

Revision ID: 9659286455c8
Revises: 56456bc75593
Create Date: 2022-02-09 20:26:50.531368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9659286455c8'
down_revision = '56456bc75593'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('user_cancel_task_reason', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('tasks', 'user_cancel_task_reason')
