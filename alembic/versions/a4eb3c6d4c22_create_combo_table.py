"""create combo table

Revision ID: a4eb3c6d4c22
Revises: 4ed62b4deb17
Create Date: 2021-11-02 16:35:59.391965

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4eb3c6d4c22'
down_revision = '4ed62b4deb17'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'combos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('title', sa.String),
        sa.Column('detail', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('image', sa.String),
        sa.Column('products', sa.JSON),
        sa.Column('total_money', sa.Float),
        sa.Column('total_money_sale', sa.Float),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    op.drop_table('combos')
