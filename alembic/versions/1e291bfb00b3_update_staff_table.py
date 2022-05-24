"""update staff table

Revision ID: 1e291bfb00b3
Revises: 9dac3b1eb26b
Create Date: 2022-01-12 23:17:25.172215

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e291bfb00b3'
down_revision = '9dac3b1eb26b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('staffs', sa.Column('province', sa.String(length=100), nullable=False, server_default='Chưa chọn'))
    op.add_column('staffs', sa.Column('district', sa.String(length=100), nullable=False, server_default='Chưa chọn'))

def downgrade():
    op.drop_column('staffs', 'province')
    op.drop_column('staffs', 'district')
