"""create notificaton table

Revision ID: c79cb4c386b5
Revises: 1ee98f62326d
Create Date: 2022-01-24 13:15:57.260545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c79cb4c386b5'
down_revision = '1ee98f62326d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'system_notification',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.TEXT, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('exp_at', sa.DateTime, nullable=False),
        sa.Column('notification_type', sa.String(length=30), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
    )
    op.create_table(
        'user_and_staff_notification',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('message', sa.TEXT, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('exp_at', sa.DateTime, nullable=False),
        sa.Column('notification_type', sa.String(length=30), nullable=False),
        sa.Column('priority', sa.String(length=20), nullable=False),
    )


def downgrade():
    op.drop_table('system_notification')
    op.drop_table('user_and_staff_notification')
