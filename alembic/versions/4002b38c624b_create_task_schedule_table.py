"""create task schedule table

Revision ID: 4002b38c624b
Revises: de80b6d9696b
Create Date: 2022-03-13 23:02:29.373908

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4002b38c624b'
down_revision = 'de80b6d9696b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'task_schedules',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('f_user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('f_staff_id', sa.Integer, sa.ForeignKey('staffs.id')),
        sa.Column('f_task_id', sa.Integer, sa.ForeignKey('tasks.id')),
        sa.Column('task_id', sa.String, nullable=False),
        sa.Column('type_task', sa.String, nullable=False),
        sa.Column('schedule_status', sa.Integer),
        sa.Column('time_from', sa.DateTime),
        sa.Column('time_to', sa.DateTime),
        sa.Column('note', sa.String, nullable=True, default=None),
        sa.Column('cancel_reason', sa.String, nullable=True, default=None),
        sa.Column('comment', sa.String, nullable=True, default=None),
        sa.Column('schedule_history', sa.JSON, nullable=True, default=[]),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
