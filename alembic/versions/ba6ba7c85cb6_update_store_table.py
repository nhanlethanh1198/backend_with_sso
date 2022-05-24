"""Update store table

Revision ID: ba6ba7c85cb6
Revises: f058243ad36f
Create Date: 2022-02-08 20:17:40.389395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6ba7c85cb6'
down_revision = 'f058243ad36f'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('stores', 'district')
    op.drop_column('stores', 'city')
    op.add_column('stores', sa.Column('province_code', sa.Integer, nullable=True))
    op.add_column('stores', sa.Column('district_code', sa.Integer, nullable=True))
    op.create_foreign_key(
        constraint_name='stores_province_code_fkey',
        source_table='stores',
        referent_table='location_provinces',
        local_cols=['province_code'],
        remote_cols=['code'],
    )
    op.create_foreign_key(
        constraint_name='stores_district_code_fkey',
        source_table='stores',
        referent_table='location_districts',
        local_cols=['district_code'],
        remote_cols=['code'],
    )


def downgrade():
    op.drop_column('stores', 'province_code')
    op.drop_column('stores', 'district_code')
    op.drop_constraint('stores_province_code_fkey', 'stores', type_='foreignkey')
    op.drop_constraint('stores_district_code_fkey', 'stores', type_='foreignkey')
