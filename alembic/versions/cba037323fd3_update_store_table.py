"""update_store_table

Revision ID: cba037323fd3
Revises: 8c77223bf63b
Create Date: 2022-01-03 14:53:54.475095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cba037323fd3'
down_revision = '8c77223bf63b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stores', sa.Column('avatar', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('stores', 'avatar')
