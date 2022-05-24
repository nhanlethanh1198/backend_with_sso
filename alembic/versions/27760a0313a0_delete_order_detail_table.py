"""delete order detail table

Revision ID: 27760a0313a0
Revises: 5e8142fe4b50
Create Date: 2022-02-21 13:46:42.385597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27760a0313a0'
down_revision = '5e8142fe4b50'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('detail_orders')


def downgrade():
    pass
