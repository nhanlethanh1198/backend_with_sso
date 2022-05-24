"""create task table

Revision ID: 751b008e33b2
Revises: 95684cae6e2c
Create Date: 2021-07-03 22:46:51.206598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6075'
down_revision = '19307d2e6074'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('type_task', sa.String),
        sa.Column('service_id', sa.String),
        sa.Column('user_id', sa.String),
        sa.Column('fullname', sa.String),
        sa.Column('phone', sa.String),
        sa.Column('address', sa.String),
        sa.Column('start_date', sa.DateTime, nullable=True, default=None),
        sa.Column('end_date', sa.DateTime, nullable=True, default=None),
        sa.Column('start_time', sa.String, nullable=True, default=None),
        sa.Column('end_time', sa.String, nullable=True, default=None),
        sa.Column('total_price', sa.Float),
        sa.Column('fee_tool', sa.Float, nullable=True, default=None),
        sa.Column('type_package', sa.String, nullable=True, default=None),
        sa.Column('is_choice_staff_favorite', sa.Boolean, default=False),
        sa.Column('is_choice_staff_manual', sa.Boolean, default=False),
        sa.Column('status', sa.Integer),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )

def downgrade():
    pass
