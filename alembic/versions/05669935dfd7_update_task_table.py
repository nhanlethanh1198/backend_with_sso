"""Update Task Table

Revision ID: 05669935dfd7
Revises: caacca052c59
Create Date: 2022-01-13 14:18:55.445321

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05669935dfd7'
down_revision = 'caacca052c59'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('tasks', 'start_date')
    op.drop_column('tasks', 'end_date')
    op.add_column('tasks', sa.Column('staff_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        constraint_name='fk_tasks_staff_id',
        source_table='tasks',
        referent_table='staffs',
        local_cols=['staff_id'],
        remote_cols=['id'],
    )


def downgrade():
    pass
