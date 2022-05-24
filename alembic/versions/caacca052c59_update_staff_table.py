"""update staff table

Revision ID: caacca052c59
Revises: 1e291bfb00b3
Create Date: 2022-01-13 10:45:49.122688

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'caacca052c59'
down_revision = '1e291bfb00b3'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('staffs', 'province')
    op.drop_column('staffs', 'district')
    op.add_column('staffs', sa.Column('province_code', sa.Integer(), nullable=True))
    op.add_column('staffs', sa.Column('district_code', sa.Integer(), nullable=True))
    op.create_foreign_key(constraint_name='fk_staff_province_code', source_table='staffs',
                          referent_table='location_provinces', local_cols=['province_code'], remote_cols=['code'])
    op.create_foreign_key(constraint_name='fk_staff_district_code', source_table='staffs',
                          referent_table='location_districts', local_cols=['district_code'], remote_cols=['code'])


def downgrade():
    pass
