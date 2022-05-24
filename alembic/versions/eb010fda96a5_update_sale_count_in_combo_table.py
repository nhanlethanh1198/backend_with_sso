"""update sale_count in combo table 

Revision ID: eb010fda96a5
Revises: fc34b1de5979
Create Date: 2022-01-08 17:19:47.413993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb010fda96a5'
down_revision = 'fc34b1de5979'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('combos', 'sale_count')
    op.add_column('combos', sa.Column('sale_count', sa.Integer(), server_default='0', nullable=False))


def downgrade():
    pass
