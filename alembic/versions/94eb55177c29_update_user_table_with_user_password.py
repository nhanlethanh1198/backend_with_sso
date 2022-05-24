"""update user table with user password

Revision ID: 94eb55177c29
Revises: 07abbcf1e8e0
Create Date: 2022-02-22 23:58:48.227472

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '94eb55177c29'
down_revision = '07abbcf1e8e0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('hashed_password', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('users', 'hashed_password')
