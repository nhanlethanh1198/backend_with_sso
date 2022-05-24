"""change column name in stores table

Revision ID: fde7527d400c
Revises: b3ff4a244ffe
Create Date: 2022-01-06 19:35:26.460732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fde7527d400c'
down_revision = 'b3ff4a244ffe'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(table_name='stores', column_name='dictrict', new_column_name='district', nullable=True)


def downgrade():
    pass
