"""update combo table

Revision ID: 78515b72d921
Revises: 2090f9e20414
Create Date: 2022-01-11 21:00:15.177662

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78515b72d921'
down_revision = '2090f9e20414'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('combos', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('note', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('tag', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('brand', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('guide', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('preserve', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('made_in', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('made_by', sa.Text(), nullable=True))
    op.add_column('combos', sa.Column('day_to_shipping', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('combos', 'description')
    op.drop_column('combos', 'note')
    op.drop_column('combos', 'tag')
    op.drop_column('combos', 'brand')
    op.drop_column('combos', 'guide')
    op.drop_column('combos', 'preserve')
    op.drop_column('combos', 'made_in')
    op.drop_column('combos', 'made_by')
    op.drop_column('combos', 'day_to_shipping')
