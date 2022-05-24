"""update_detail_order_table

Revision ID: 115c90eecf07
Revises: 198d5d5ae7b7
Create Date: 2021-12-13 11:14:23.792607

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import table


# revision identifiers, used by Alembic.
revision = '115c90eecf07'
down_revision = '198d5d5ae7b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('detail_orders', sa.Column(
        'user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        constraint_name='detail_order_user_id_fkey',
        source_table='detail_orders',
        referent_table='users',
        local_cols=['user_id'],
        remote_cols=['id']
    )
    op.create_foreign_key(
        constraint_name='detail_order_code_fkey',
        source_table='detail_orders',
        referent_table='products',
        local_cols=['code'],
        remote_cols=['code']
    )


def downgrade():
    op.drop_constraint(
        constraint_name='detail_order_user_id_fkey',
        table_name='detail_orders',
        type_='foreignkey'
    )
    op.drop_column('detail_orders', 'user_id')
    op.drop_constraint(
        constraint_name='detail_order_code_fkey',
        table_name='detail_orders',
        type_='foreignkey'
    )
