"""update_staff_vote

Revision ID: 6c60630c10f2
Revises: 11b182cbb18f
Create Date: 2021-12-13 21:14:35.809868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c60630c10f2'
down_revision = '11b182cbb18f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('staffs', sa.Column('skill_score_count',
                  sa.Integer(), server_default='0', nullable=False))
    op.add_column('staffs', sa.Column('attitude_score_count',
                  sa.Integer(), server_default='0', nullable=False))
    op.add_column('staffs', sa.Column('contentment_score_count',
                  sa.Integer(), server_default='0', nullable=False))


def downgrade():
    op.drop_column('staffs', 'skill_score_count')
    op.drop_column('staffs', 'attitude_score_count')
    op.drop_column('staffs', 'contentment_score_count')
