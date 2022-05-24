"""update_tasks_table

Revision ID: a5c80b9df962
Revises: ac4dfde5038a
Create Date: 2021-12-22 14:37:28.880255

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5c80b9df962'
down_revision = 'ac4dfde5038a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(table_name='tasks', column_name='user_id')
    op.add_column('tasks', sa.Column('user_id', sa.Integer, nullable=True))
    op.create_foreign_key(constraint_name='fk_tasks_user_id', source_table='tasks',
                          referent_table='users', local_cols=['user_id'], remote_cols=['id'])


def downgrade():
    pass
