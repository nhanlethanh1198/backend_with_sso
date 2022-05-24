"""create banner table

Revision ID: c6a02f7c5f1d
Revises: a6564584ce16
Create Date: 2021-11-06 13:52:53.485881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6a02f7c5f1d'
down_revision = 'a6564584ce16'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'banners',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('image', sa.String),
        sa.Column('category_id', sa.Integer),
        sa.Column('is_active', sa.Boolean),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
