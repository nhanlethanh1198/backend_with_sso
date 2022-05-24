"""update_store_location

Revision ID: b3ff4a244ffe
Revises: 6ee41b702411
Create Date: 2022-01-06 13:29:32.358522

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3ff4a244ffe'
down_revision = '6ee41b702411'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(column_name='address', table_name='stores')
    op.add_column('stores', sa.Column('address', sa.String, nullable=True))
    op.add_column('stores', sa.Column('dictrict', sa.String, nullable=True))
    op.add_column('stores', sa.Column('city', sa.String, nullable=True))


def downgrade():
    op.drop_column(column_name='address', table_name='stores')
    op.drop_column(column_name='dictrict', table_name='stores')
    op.drop_column(column_name='city', table_name='stores')
