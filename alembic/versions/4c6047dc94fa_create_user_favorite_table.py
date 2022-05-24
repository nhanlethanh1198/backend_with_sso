"""create user_favorite_table

Revision ID: 4c6047dc94fa
Revises: bc4d30d72bef
Create Date: 2022-02-11 10:09:19.475885

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c6047dc94fa'
down_revision = 'bc4d30d72bef'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_favorites",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('product_id', sa.Integer, sa.ForeignKey('products.id'), nullable=True),
        sa.Column('combo_id', sa.Integer, sa.ForeignKey('combos.id'), nullable=True),
        sa.Column('store_id', sa.Integer, sa.ForeignKey('stores.id'), nullable=True),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default='now()'),
    )


def downgrade():
    op.drop_table('user_favorites')
