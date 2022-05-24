"""add foreign_key to OrderTable

Revision ID: 198d5d5ae7b7
Revises: 967eb1978ed7
Create Date: 2021-12-12 21:49:37.430113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198d5d5ae7b7'
down_revision = '967eb1978ed7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        constraint_name="user_id_fkey",
        source_table="orders",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"]
    )


def downgrade():
    op.drop_constraint(constraint_name="user_id_fkey", table_name="orders", type_="foreignkey")
