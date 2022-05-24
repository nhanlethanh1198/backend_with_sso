"""create store table

Revision ID: e887014119d1
Revises: f42fb997b100
Create Date: 2021-11-14 11:38:59.234323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e887014119d1'
down_revision = 'f42fb997b100'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('address', sa.String),
        sa.Column('phone', sa.String),
        sa.Column('email', sa.String, nullable=True, default=None),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
