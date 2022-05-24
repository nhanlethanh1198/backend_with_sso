"""create staff table

Revision ID: 95684cae6e2c
Revises: 592501e0d619
Create Date: 2021-07-01 23:12:21.443723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6076'
down_revision = '19307d2e6075'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'staffs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('role', sa.String, default="staff"),
        sa.Column('fullname', sa.String),
        sa.Column('dob', sa.DateTime),
        sa.Column('address', sa.String),
        sa.Column('email', sa.String),
        sa.Column('phone', sa.String, unique=True),
        sa.Column('hash_password', sa.String),
        sa.Column('id_card', sa.String),
        sa.Column('avatar_img', sa.String),
        sa.Column('id_card_img_1', sa.String),
        sa.Column('id_card_img_2', sa.String),
        sa.Column('status', sa.String),
        sa.Column('join_from_date', sa.DateTime),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

    op.create_table(
        'star_staffs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('staff_id', sa.String),
        sa.Column('star', sa.Integer),
        sa.Column('user_id', sa.Integer),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade():
    pass
