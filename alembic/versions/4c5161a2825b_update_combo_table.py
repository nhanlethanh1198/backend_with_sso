"""update combo table

Revision ID: 4c5161a2825b
Revises: 562d78f38c70
Create Date: 2022-01-17 17:58:17.405829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c5161a2825b'
down_revision = '562d78f38c70'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('combos', sa.Column('code', sa.String(length=10), nullable=True, unique=True))


def downgrade():
    op.drop_column('combos', 'code')
