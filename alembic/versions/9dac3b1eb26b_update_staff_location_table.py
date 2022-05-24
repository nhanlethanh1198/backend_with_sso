"""update staff location table

Revision ID: 9dac3b1eb26b
Revises: 2afdd3c5cfbd
Create Date: 2022-01-12 17:45:13.253376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9dac3b1eb26b'
down_revision = '2afdd3c5cfbd'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('staff_location', 'city', nullable=False, new_column_name='province')


def downgrade():
    pass
