"""update staffs table

Revision ID: 1ee98f62326d
Revises: ba5c32275e70
Create Date: 2022-01-24 11:51:50.168078

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1ee98f62326d'
down_revision = 'ba5c32275e70'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('staffs', sa.Column('gender', sa.String(length=10), server_default='male', nullable=False))
    op.add_column('staffs', sa.Column('age', sa.Integer(), server_default='0', nullable=False))


def downgrade():
    op.drop_column('staffs', 'gender')
    op.drop_column('staffs', 'age')