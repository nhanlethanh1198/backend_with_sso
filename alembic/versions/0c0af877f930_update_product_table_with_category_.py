"""update product table with category foregin key

Revision ID: 0c0af877f930
Revises: 97bbc72e1bb5
Create Date: 2022-03-03 17:09:48.475852

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0c0af877f930'
down_revision = '97bbc72e1bb5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('fk_product_category', 'products', 'categories', ['category_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_product_category', 'products', type_='foreignkey')
