"""update combos table

Revision ID: 4bf9a5f5a90a
Revises: e887014119d1
Create Date: 2021-11-16 17:16:55.337896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bf9a5f5a90a'
down_revision = 'e887014119d1'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('combos')


def downgrade():
    op.drop_table('combos')
