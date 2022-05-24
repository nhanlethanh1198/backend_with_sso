"""vote_combo

Revision ID: fc34b1de5979
Revises: cee7e3ed5c16
Create Date: 2022-01-08 14:39:24.720497

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'fc34b1de5979'
down_revision = 'cee7e3ed5c16'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('combo_user_votes',
                    sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
                    sa.Column('combo_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('comment', sa.Unicode(length=255), nullable=True),
                    sa.Column('vote_score', sa.Integer(), nullable=True),
                    sa.Column('tags', postgresql.ARRAY(sa.Unicode), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default='now()', nullable=False),
                    sa.ForeignKeyConstraint(['combo_id'], ['combos.id']),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'])
                    )
    op.add_column('combos', sa.Column('sale_count', sa.Integer(), nullable=True))
    op.add_column('combos', sa.Column('vote_count_updated_at', sa.DateTime(), server_default='now()', nullable=True))
    op.add_column('combos', sa.Column('vote_count', sa.Integer, server_default="0"))
    op.add_column('combos', sa.Column('vote_average_score', sa.Float, server_default="0.0"))
    op.add_column('combos', sa.Column('vote_one_star_count', sa.Integer, server_default="0"))
    op.add_column('combos', sa.Column('vote_two_star_count', sa.Integer, server_default="0"))
    op.add_column('combos', sa.Column('vote_three_star_count', sa.Integer, server_default="0"))
    op.add_column('combos', sa.Column('vote_four_star_count', sa.Integer, server_default="0"))
    op.add_column('combos', sa.Column('vote_five_star_count', sa.Integer, server_default="0"))

def downgrade():
    op.drop_table('combo_user_votes')
    op.drop_column('combos', 'sale_count')
    op.drop_column('combos', 'vote_count_updated_at')
    op.drop_column('combos', 'vote_count')
    op.drop_column('combos', 'vote_average_score')
    op.drop_column('combos', 'vote_one_star_count')
    op.drop_column('combos', 'vote_two_star_count')
    op.drop_column('combos', 'vote_three_star_count')
    op.drop_column('combos', 'vote_four_star_count')
    op.drop_column('combos', 'vote_five_star_count')