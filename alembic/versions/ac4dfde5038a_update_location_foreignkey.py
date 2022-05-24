"""update_location_foreignkey

Revision ID: ac4dfde5038a
Revises: 6c60630c10f2
Create Date: 2021-12-21 13:38:11.829505

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac4dfde5038a'
down_revision = '6c60630c10f2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(constraint_name='fk_locations_user_id', source_table='locations',
                          referent_table='users', local_cols=['user_id'], remote_cols=['id'])


def downgrade():
    op.drop_constraint(constraint_name='fk_locations_user_id',
                       table_name='locations', type_='foreignkey')
