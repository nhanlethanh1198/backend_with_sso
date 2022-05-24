"""update product table

Revision ID: e36c37afb053
Revises: 27e1eb98314e
Create Date: 2022-03-01 23:36:53.648566

"""
import sqlalchemy.dialects.postgresql as pg
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e36c37afb053'
down_revision = '27e1eb98314e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('products', 'image_list', type_=pg.JSONB())


def downgrade():
    pass
