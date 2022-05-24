"""create favorite staffs of user

Revision ID: 1262089b87f0
Revises: 05669935dfd7
Create Date: 2022-01-14 21:09:06.594651

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1262089b87f0'
down_revision = '05669935dfd7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('favorite_staffs_of_user',
                    sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('staff_id', sa.Integer(), nullable=False),
                    sa.Column('is_favorite', sa.Boolean(), nullable=False, server_default=sa.text('true')),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='now()'),
                    sa.ForeignKeyConstraint(['staff_id'], ['staffs.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    )


def downgrade():
    op.drop_table('favorite_staffs_of_user')
