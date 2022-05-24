"""update order table with cancel reason

Revision ID: 5e8142fe4b50
Revises: 4c6047dc94fa
Create Date: 2022-02-17 14:34:11.931443

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5e8142fe4b50'
down_revision = '4c6047dc94fa'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('orders', sa.Column('cancel_reason', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('orders', 'cancel_reason')
