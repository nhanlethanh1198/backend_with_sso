"""create location

Revision ID: a6564584ce16
Revises: a4eb3c6d4c22
Create Date: 2021-11-04 15:29:25.996909

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6564584ce16'
down_revision = 'a4eb3c6d4c22'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'locations',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
        sa.Column('type_location', sa.String),
        sa.Column('title_location', sa.String),
        sa.Column('address', sa.String),
        sa.Column('district', sa.String),
        sa.Column('city', sa.String),
        sa.Column('country', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
