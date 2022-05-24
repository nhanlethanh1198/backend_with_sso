"""update product table

Revision ID: a6eeb149d77f
Revises: f4a4abd79c96
Create Date: 2021-11-22 16:18:36.682992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6eeb149d77f'
down_revision = 'f4a4abd79c96'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("products", "category_id")
    op.add_column('products', sa.Column('category_id', sa.Integer))

def downgrade():
    pass
