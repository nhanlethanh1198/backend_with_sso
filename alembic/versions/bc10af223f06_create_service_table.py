"""create service table

Revision ID: bc10af223f06
Revises: 9b027e18fb26
Create Date: 2021-06-29 20:39:54.850656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6078'
down_revision = '19307d2e6077'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'services',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String),
        sa.Column('extra_title', sa.String, nullable=True),
        sa.Column('image', sa.String),
        sa.Column('tag', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
