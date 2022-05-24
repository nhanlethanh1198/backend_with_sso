"""update product of combo table

Revision ID: cee7e3ed5c16
Revises: 8abb6422455a
Create Date: 2022-01-07 14:59:20.547773

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cee7e3ed5c16'
down_revision = '8abb6422455a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(table_name='product_of_combo', column_name='id')
    op.add_column('product_of_combo', sa.Column('id', sa.Integer(), primary_key=True, nullable=False))


def downgrade():
    op.drop_column(table_name='product_of_combo', column_name='id')
