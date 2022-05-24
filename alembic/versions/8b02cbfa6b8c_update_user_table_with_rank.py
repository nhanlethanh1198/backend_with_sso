"""update user table with rank

Revision ID: 8b02cbfa6b8c
Revises: 94eb55177c29
Create Date: 2022-02-23 00:17:18.189032

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '8b02cbfa6b8c'
down_revision = '94eb55177c29'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'rank', server_default='Đồng')


def downgrade():
    pass
