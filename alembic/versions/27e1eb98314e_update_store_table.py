"""update store table

Revision ID: 27e1eb98314e
Revises: 91b7becd878c
Create Date: 2022-03-01 16:00:07.829466

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '27e1eb98314e'
down_revision = '91b7becd878c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('stores', sa.Column('description', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('stores', 'description')
