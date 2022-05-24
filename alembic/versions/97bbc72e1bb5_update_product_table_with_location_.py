"""update product table with location foreign key

Revision ID: 97bbc72e1bb5
Revises: e36c37afb053
Create Date: 2022-03-03 17:06:38.715431

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '97bbc72e1bb5'
down_revision = 'e36c37afb053'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key('fk_product_location', 'products', 'location_provinces', ['location'], ['code'])


def downgrade():
    op.drop_constraint('fk_product_location', 'products', type_='foreignkey')
