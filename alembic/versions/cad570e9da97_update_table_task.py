"""update table task

Revision ID: cad570e9da97
Revises: 1262089b87f0
Create Date: 2022-01-16 23:08:08.736606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cad570e9da97'
down_revision = '1262089b87f0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tasks', sa.Column('voucher', sa.String, nullable=True))
    op.add_column('tasks', sa.Column('note', sa.String, nullable=True))
    op.add_column('tasks', sa.Column('payment_method', sa.String, nullable=True, default="cash"))
    op.add_column('tasks', sa.Column('has_tool', sa.Boolean, default=False))



def downgrade():
    pass
