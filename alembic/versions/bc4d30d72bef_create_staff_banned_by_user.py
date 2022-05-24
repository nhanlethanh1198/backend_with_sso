"""create staff_banned_by_user

Revision ID: bc4d30d72bef
Revises: 9659286455c8
Create Date: 2022-02-09 20:38:03.867076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc4d30d72bef'
down_revision = '9659286455c8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("staff_banned_by_user",
                    sa.Column("id", sa.Integer(), nullable=False, autoincrement=True, primary_key=True),
                    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
                    sa.Column("staff_id", sa.Integer(), sa.ForeignKey("staffs.id")),
                    sa.Column("created_at", sa.DateTime(), server_default='now()'),
                    )


def downgrade():
    op.drop_table("staff_banned_by_user")
