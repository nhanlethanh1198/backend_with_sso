"""update product table

Revision ID: 14d8363bdd77
Revises: c6a02f7c5f1d
Create Date: 2021-11-09 21:05:13.362417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14d8363bdd77'
down_revision = 'c6a02f7c5f1d'
branch_labels = None
depends_on = None




def downgrade():
    op.drop_column("products", "extra")
    op.drop_column("products", "price")
def upgrade():
    op.add_column('products', sa.Column('price_sale', sa.Float))
    op.add_column('products', sa.Column('unit', sa.String))
    op.add_column('products', sa.Column('weight', sa.Integer))
    op.add_column('products', sa.Column('stock', sa.Integer))
