"""update star_staffs table

Revision ID: d52af2f8a5da
Revises: 115c90eecf07
Create Date: 2021-12-13 17:01:36.101626

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd52af2f8a5da'
down_revision = '115c90eecf07'
branch_labels = None
depends_on = None


def upgrade():
    # update star_staffs table
    op.drop_table('star_staffs')
    op.create_table(
        'star_staffs',
        sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
        sa.Column('staff_id', sa.Integer(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('comment', sa.Unicode(length=255), nullable=True),
        sa.Column('vote_score', sa.Integer(), server_default='0', nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Unicode), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default='now()', nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default='now()', nullable=False),
    )
    op.create_foreign_key(
        constraint_name='star_staffs_staff_id_fkey',
        source_table='star_staffs',
        referent_table='staffs',
        local_cols=['staff_id'],
        remote_cols=['id'],
    )
    op.create_foreign_key(
        constraint_name='star_staffs_user_id_fkey',
        source_table='star_staffs',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id'],
    )


def downgrade():
    pass
