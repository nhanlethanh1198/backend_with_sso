"""create task of staff table

Revision ID: 2090f9e20414
Revises: 8c799c6b8090
Create Date: 2022-01-11 18:15:32.194128

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2090f9e20414'
down_revision = '8c799c6b8090'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(table_name='tasks', column_name='service_id')
    op.create_table('task_of_staff',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('task_id', sa.Integer(), nullable=False),
                    sa.Column('task_type', sa.String(length=50), nullable=False),
                    sa.Column('task_status', sa.Integer(), nullable=False, server_default='1'),
                    sa.Column('staff_id', sa.Integer(), nullable=True),
                    sa.Column('staff_accept_time', sa.DateTime(), nullable=True),
                    sa.Column('staff_start_time', sa.DateTime(), nullable=True),
                    sa.Column('staff_finish_time', sa.DateTime(), nullable=True),
                    sa.Column('staff_status', sa.Integer(), nullable=True),
                    )
    op.create_foreign_key(constraint_name='fk_task_of_staff_task_id', source_table='task_of_staff', referent_table='tasks', local_cols=['task_id'], remote_cols=['id'])
    op.create_foreign_key(constraint_name='fk_task_of_staff_staff_id', source_table='task_of_staff', referent_table='staffs', local_cols=['staff_id'], remote_cols=['id'])


def downgrade():
    op.drop_table('task_of_staff')
