"""update user table with avatar

Revision ID: 44fbc5bac5b5
Revises: d674c11fbba2
Create Date: 2022-02-09 17:26:15.166989

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '44fbc5bac5b5'
down_revision = 'd674c11fbba2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('avatar', sa.String(length=100), nullable=True))


def downgrade():
    op.drop_column('users', 'avatar')
