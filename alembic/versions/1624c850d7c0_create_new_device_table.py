"""create new device table

Revision ID: 1624c850d7c0
Revises: abbd220cb60b
Create Date: 2022-01-26 11:09:16.673673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1624c850d7c0'
down_revision = 'abbd220cb60b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("user_devices",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
                    sa.Column('device_info', sa.String(length=100), nullable=False),
                    sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
                    sa.Column('created_at', sa.DateTime, nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime, nullable=False, server_default='now()'),
                    sa.Column('FCM_token', sa.String(length=255), nullable=False),
                    )
    op.create_table("staff_devices",
                    sa.Column("id", sa.Integer, primary_key=True),
                    sa.Column('staff_id', sa.Integer, sa.ForeignKey('staffs.id'), nullable=False),
                    sa.Column('device_info', sa.String(length=100), nullable=False),
                    sa.Column('is_active', sa.Boolean, nullable=False, server_default='true'),
                    sa.Column('created_at', sa.DateTime, nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime, nullable=False, server_default='now()'),
                    sa.Column('FCM_token', sa.String(length=255), nullable=False),
                    )


def downgrade():
    op.drop_table("user_devices")
    op.drop_table("staff_devices")
