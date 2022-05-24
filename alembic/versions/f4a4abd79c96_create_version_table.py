"""create version table

Revision ID: f4a4abd79c96
Revises: 3924e6ae68a7
Create Date: 2021-11-20 17:11:21.345364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4a4abd79c96'
down_revision = '3924e6ae68a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'versions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ios', sa.String),
        sa.Column('android', sa.String),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
