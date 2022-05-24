"""create promotion table

Revision ID: 592501e0d619
Revises: bc10af223f06
Create Date: 2021-06-29 22:45:18.774393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6077'
down_revision = '19307d2e6076'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'promotions',
        sa.Column('id', sa.Integer, primary_key=True),

        sa.Column('code', sa.String),
        sa.Column('image', sa.String),
        sa.Column('title', sa.String),
        sa.Column('time_to', sa.DateTime),
        sa.Column('time_from', sa.DateTime),
        sa.Column('detail', sa.String, nullable=True),
        sa.Column('rule', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),

        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
