"""Update Combo Table

Revision ID: a8f21bbfccad
Revises: a6eeb149d77f
Create Date: 2021-11-23 20:45:56.358085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8f21bbfccad'
down_revision = 'a6eeb149d77f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('combos', sa.Column(
        'recommend_price', sa.Float(), nullable=False))


def downgrade():
    pass
