"""drop services table

Revision ID: 8c799c6b8090
Revises: eb010fda96a5
Create Date: 2022-01-11 17:48:08.071924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c799c6b8090'
down_revision = 'eb010fda96a5'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('services')
    
def downgrade():
    pass
