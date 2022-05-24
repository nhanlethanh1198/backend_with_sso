"""create location provices table

Revision ID: 2afdd3c5cfbd
Revises: 78515b72d921
Create Date: 2022-01-12 16:10:49.763962

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2afdd3c5cfbd'
down_revision = '78515b72d921'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('location_provinces',
                    sa.Column('code', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('name_en', sa.String(length=255), nullable=False),
                    sa.Column('fullname', sa.String(length=255), nullable=False),
                    sa.Column('fullname_en', sa.String(length=255), nullable=False),
                    sa.Column('code_name', sa.String(length=255), nullable=False),
                    )
    op.create_table('location_districts',
                   sa.Column('code', sa.Integer(), nullable=False, primary_key=True),
                   sa.Column('name', sa.String(length=255), nullable=False),
                   sa.Column('name_en', sa.String(length=255), nullable=False),
                   sa.Column('fullname', sa.String(length=255), nullable=False),
                   sa.Column('fullname_en', sa.String(length=255), nullable=False),
                   sa.Column('code_name', sa.String(length=255), nullable=False),
                   sa.Column('province_code', sa.Integer(), nullable=False),
                   )
    op.create_foreign_key(
        constraint_name='fk_district_province',
        source_table='location_districts',
        referent_table='location_provinces',
        local_cols=['province_code'],
        remote_cols=['code'],
    )

def downgrade():
    op.drop_table('location_districts')
    op.drop_table('location_provinces')
