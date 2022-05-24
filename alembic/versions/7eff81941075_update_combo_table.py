"""update combo table

Revision ID: 7eff81941075
Revises: 4002b38c624b
Create Date: 2022-03-14 12:42:12.819469

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '7eff81941075'
down_revision = '4002b38c624b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('combos', sa.Column('f_location', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_combo_provinces', 'combos', 'location_provinces', ['f_location'], ['code'])


def downgrade():
    op.drop_column('combos', 'f_location')
    op.drop_constraint('fk_combo_provinces', 'combos', type_='foreignkey')
