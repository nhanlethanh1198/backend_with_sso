"""update task table

Revision ID: 46e31318e40c
Revises: 1262089b87f0
Create Date: 2022-01-16 23:22:34.130674

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46e31318e40c'
down_revision = '1262089b87f0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('tasks', 'staff_id')
    op.drop_column('tasks', 'is_choice_staff_manual')
    op.add_column('tasks', sa.Column('staff_id', sa.Integer(), nullable=True))
    op.create_foreign_key(constraint_name='fk_tasks_staff_id', source_table='tasks',
                          referent_table='staffs', local_cols=['staff_id'], remote_cols=['id'])


def downgrade():
    pass
