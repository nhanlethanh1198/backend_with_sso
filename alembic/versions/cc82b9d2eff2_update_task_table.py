"""update task table

Revision ID: cc82b9d2eff2
Revises: 0e57d069d96e
Create Date: 2022-01-19 22:17:42.736946

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc82b9d2eff2'
down_revision = '0e57d069d96e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('tasks', 'type_package')


def downgrade():
    pass