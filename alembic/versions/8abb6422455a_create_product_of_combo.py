"""Create product_of_combo

Revision ID: 8abb6422455a
Revises: fde7527d400c
Create Date: 2022-01-07 07:19:11.545177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8abb6422455a'
down_revision = 'fde7527d400c'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column(table_name='combos', column_name='products')
    op.create_table('product_of_combo',
                    sa.Column('id', sa.Integer(), nullable=False, autoincrement=True),
                    sa.Column('combo_id', sa.Integer(), nullable=False),
                    sa.Column('product_id', sa.Integer(), nullable=False),
                    sa.Column('count', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False, server_default='now()'),
                    sa.Column('updated_at', sa.DateTime(), nullable=False, server_default='now()'),
                    )
    op.create_foreign_key(constraint_name='fk_product_of_combo_combo_id', source_table='product_of_combo', referent_table='combos', local_cols=['combo_id'], remote_cols=['id'])
    op.create_foreign_key(constraint_name='fk_product_of_combo_product_id', source_table='product_of_combo', referent_table='products', local_cols=['product_id'], remote_cols=['id'])


def downgrade():
    op.drop_table('product_of_combo')
