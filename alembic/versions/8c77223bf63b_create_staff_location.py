"""create staff_location

Revision ID: 8c77223bf63b
Revises: f162eab512cf
Create Date: 2022-01-03 11:44:33.179835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c77223bf63b'
down_revision = 'f162eab512cf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('staff_location',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('staff_id', sa.Integer(), nullable=False),
                    sa.Column('type_location', sa.String(length=255), nullable=False, server_default='home'),
                    sa.Column('title_location', sa.String(length=255), nullable=False, server_default='home'),
                    sa.Column('address', sa.String(length=255), nullable=True),
                    sa.Column('district', sa.String(length=255), nullable=True),
                    sa.Column('city', sa.String(length=255), nullable=True),
                    sa.Column('country', sa.String(length=255), nullable=True, server_default='Vietnam'),
                    sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
                    sa.Column('created_at', sa.DateTime(), nullable=True, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime(), nullable=True, server_default='now()'),
                    )
    op.create_foreign_key(constraint_name='fk_staff_location_staff_id',
                          source_table='staff_location',
                          referent_table='staffs',
                          local_cols=['staff_id'],
                          remote_cols=['id']
                          )


def downgrade():
    op.drop_table('staff_location')
