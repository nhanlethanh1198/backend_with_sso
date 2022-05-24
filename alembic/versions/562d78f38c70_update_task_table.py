"""update task table

Revision ID: 562d78f38c70
Revises: fba243748d96
Create Date: 2022-01-17 13:49:40.882665

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '562d78f38c70'
down_revision = 'fba243748d96'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('discount', sa.Float(), nullable=False, server_default='0'))


def downgrade():
    op.drop_column(table_name='tasks', column_name='discount')
