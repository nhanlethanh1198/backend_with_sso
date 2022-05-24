"""create nofitication table

Revision ID: d575a1a2a143
Revises: 7eff81941075
Create Date: 2022-03-16 23:28:04.571485

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd575a1a2a143'
down_revision = '7eff81941075'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'notifications',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('title', sa.String),
        sa.Column('content', sa.Text),
        sa.Column('image', sa.String),
        sa.Column('type', sa.String),
        sa.Column('detail', sa.JSON, nullable=True, default=None),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime),
    )


def downgrade():
    pass
