"""update col price

Revision ID: f42fb997b100
Revises: 14d8363bdd77
Create Date: 2021-11-09 21:27:41.194979

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f42fb997b100'
down_revision = '14d8363bdd77'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('products', 'price')
    op.add_column('products', sa.Column('price', sa.Float, server_default='0'))


def downgrade():
    pass
