"""create combos table

Revision ID: 3924e6ae68a7
Revises: 4bf9a5f5a90a
Create Date: 2021-11-17 12:55:31.119873

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3924e6ae68a7'
down_revision = '4bf9a5f5a90a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'combos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String),
        sa.Column('detail', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('image', sa.String),
        sa.Column('products', sa.JSON),
        sa.Column('total_money', sa.Float),
        sa.Column('total_money_sale', sa.Float),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
