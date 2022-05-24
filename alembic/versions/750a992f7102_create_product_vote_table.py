"""create product vote table

Revision ID: 750a992f7102
Revises: 67aebd1298e0
Create Date: 2021-12-08 14:34:30.952496

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '750a992f7102'
down_revision = '67aebd1298e0'
branch_labels = None
depends_on = None


def upgrade():
   op.add_column('products', sa.Column('vote_count_updated_at', sa.DateTime(), server_default='now()', nullable=True))
   op.add_column('products', sa.Column('vote_count', sa.Integer, server_default=0))
   op.add_column('products', sa.Column('vote_average_score', sa.Float, server_default=0.0))
   op.add_column('products', sa.Column('vote_one_star_count', sa.Integer, server_default=0.0))
   op.add_column('products', sa.Column('vote_two_star_count', sa.Integer, server_default=0.0))
   op.add_column('products', sa.Column('vote_three_star_count', sa.Integer, server_default=0.0))
   op.add_column('products', sa.Column('vote_four_star_count', sa.Integer, server_default=0.0))
   op.add_column('products', sa.Column('vote_five_star_count', sa.Integer, server_default=0.0))


def downgrade():
   op.drop_column('products', 'vote_count_updated_at')
   op.drop_column('products', 'vote_count')
   op.drop_column('products', 'vote_average_score')
   op.drop_column('products', 'vote_one_start_count')
   op.drop_column('products', 'vote_two_start_count')
   op.drop_column('products', 'vote_three_start_count')
   op.drop_column('products', 'vote_four_start_count')
   op.drop_column('products', 'vote_five_start_count')
    
    