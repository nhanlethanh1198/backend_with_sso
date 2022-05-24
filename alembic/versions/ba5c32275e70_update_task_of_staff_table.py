"""update task of staff table

Revision ID: ba5c32275e70
Revises: cc82b9d2eff2
Create Date: 2022-01-19 22:19:38.739598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba5c32275e70'
down_revision = 'cc82b9d2eff2'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('task_of_staff', 'task_type', nullable=True, new_column_name='type_task')
    op.add_column('task_of_staff', sa.Column('task_start_time', sa.DateTime(), nullable=True))
    op.add_column('task_of_staff', sa.Column('task_end_time', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('task_of_staff', 'task_start_time')
    op.drop_column('task_of_staff', 'task_end_time')
