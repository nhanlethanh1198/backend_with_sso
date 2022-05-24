"""add category table

Revision ID: e0b58c88a31c
Revises: 19307d2e6073
Create Date: 2021-06-21 18:26:11.824957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6079'
down_revision = '19307d2e6078'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('slug', sa.String, nullable=False),
        sa.Column('image', sa.String, nullable=False),
        sa.Column('parent_id', sa.Integer, nullable=True, default=None),
        sa.Column('has_child', sa.Boolean, nullable=True, default=False),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
