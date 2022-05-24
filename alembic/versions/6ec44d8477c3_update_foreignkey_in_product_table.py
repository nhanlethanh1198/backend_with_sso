"""update foreignkey in product table

Revision ID: 6ec44d8477c3
Revises: a5c80b9df962
Create Date: 2021-12-26 20:06:38.008010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ec44d8477c3'
down_revision = 'a5c80b9df962'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(constraint_name='fk_store_id_for_product', source_table='products',
                          referent_table='stores', local_cols=['belong_to_store'], remote_cols=['id'])


def downgrade():
    op.drop_constraint(constraint_name='fk_store_id_for_product', source_table='products',)
