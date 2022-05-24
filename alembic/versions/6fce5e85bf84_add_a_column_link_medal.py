"""Add a column link medal

Revision ID: 6fce5e85bf84
Revises: 0c0af877f930
Create Date: 2022-03-05 13:08:46.051992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fce5e85bf84'
down_revision = '0c0af877f930'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('medal_link', sa.String, nullable=True, server_default=None))


def downgrade():
    pass
