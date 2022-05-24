"""create user table

Revision ID: 19307d2e6073
Revises: 
Create Date: 2021-06-06 18:08:48.312931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6073'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(100), nullable=True),
        sa.Column('dob', sa.DateTime, nullable=True),
        sa.Column('fullname', sa.String(100), nullable=True),
        sa.Column('phone', sa.String(10), nullable=False),
        sa.Column('address', sa.String, nullable=True),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('updated_at', sa.DateTime, nullable=False)
    )


def downgrade():
    pass
