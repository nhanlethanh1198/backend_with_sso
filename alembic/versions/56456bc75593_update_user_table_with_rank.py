"""update user table with rank

Revision ID: 56456bc75593
Revises: 44fbc5bac5b5
Create Date: 2022-02-09 17:37:43.407196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56456bc75593'
down_revision = '44fbc5bac5b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('rank', sa.String(length=10), nullable=False, server_default="BRONZE"))


def downgrade():
    op.drop_column('users', 'rank')

