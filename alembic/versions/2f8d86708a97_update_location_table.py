"""update location table

Revision ID: 2f8d86708a97
Revises: 178b1d65a7ac
Create Date: 2021-11-29 08:52:16.063467

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f8d86708a97'
down_revision = '178b1d65a7ac'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('locations', sa.Column('fullname', sa.String, nullable=True))
    op.add_column('locations', sa.Column('phone', sa.String, nullable=True))

def downgrade():
    pass
