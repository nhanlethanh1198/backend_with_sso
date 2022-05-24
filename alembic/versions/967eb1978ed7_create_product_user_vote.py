"""create product user vote

Revision ID: 967eb1978ed7
Revises: 750a992f7102
Create Date: 2021-12-08 21:14:56.364829

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '967eb1978ed7'
down_revision = '750a992f7102'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product_user_vote',
                    sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
                    sa.Column('product_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.Column('comment', sa.Unicode(length=255), nullable=True),
                    sa.Column('vote_score', sa.Integer(), nullable=True),
                    sa.Column('tags', postgresql.ARRAY(sa.Unicode), nullable=True),
                    sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default='now()', nullable=False),
                    sa.ForeignKeyConstraint(['product_id'], ['products.id']),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'])
                    )


def downgrade():
    op.drop_table('product_user_vote')
