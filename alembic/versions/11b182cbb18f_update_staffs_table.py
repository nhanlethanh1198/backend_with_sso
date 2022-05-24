"""update staffs table

Revision ID: 11b182cbb18f
Revises: d52af2f8a5da
Create Date: 2021-12-13 17:13:56.000987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11b182cbb18f'
down_revision = 'd52af2f8a5da'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('staffs', sa.Column('working_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('skill_average_score', sa.Float(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('attitude_average_score', sa.Float(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('contentment_average_score', sa.Float(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_average_score', sa.Float(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_one_star_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_two_star_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_three_star_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_four_star_count', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('staffs', sa.Column('vote_five_star_count', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('staffs', 'working_count')
    op.drop_column('staffs', 'vote_count')
    op.drop_column('staffs', 'skill_average_score')
    op.drop_column('staffs', 'attitude_average_score')
    op.drop_column('staffs', 'contentment_average_score')
    op.drop_column('staffs', 'vote_average_score')
    op.drop_column('staffs', 'vote_one_star_count')
    op.drop_column('staffs', 'vote_two_star_count')
    op.drop_column('staffs', 'vote_three_star_count')
    op.drop_column('staffs', 'vote_four_star_count')
    op.drop_column('staffs', 'vote_five_star_count')

    
