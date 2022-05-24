"""create product table

Revision ID: 9b027e18fb26
Revises: b00d81710165
Create Date: 2021-06-26 09:59:24.568438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '19307d2e6074'
down_revision = '19307d2e6073'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'products',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String, unique=True),
        sa.Column('name', sa.String),
        sa.Column('slug', sa.String),
        sa.Column('avatar_img', sa.String),
        sa.Column('category_id', sa.JSON),
        sa.Column('price', sa.JSON),
        sa.Column('status', sa.Integer),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('tag', sa.String, nullable=True, default=None),
        sa.Column('image_list', sa.JSON, nullable=True, default=None),
        sa.Column('day_to_shipping', sa.String, nullable=True, default=None),
        sa.Column('description', sa.Text, nullable=True, default=None),
        sa.Column('note', sa.Text, nullable=True, default=None),
        sa.Column('tag', sa.String, nullable=True, default=None),
        sa.Column('type_product', sa.String, nullable=True, default=None),
        sa.Column('brand', sa.String, nullable=True, default=None),
        sa.Column('made_in', sa.String, nullable=True, default=None),
        sa.Column('made_by', sa.String, nullable=True, default=None),
        sa.Column('guide', sa.Text, nullable=True, default=None),
        sa.Column('preserve', sa.Text, nullable=True, default=None),
        sa.Column('location', sa.Integer, nullable=True, default=None),
        sa.Column('total_rate', sa.Integer, nullable=True, default=None),
        sa.Column('comment', sa.JSON, nullable=True, default=None),
        sa.Column('belong_to_store', sa.Integer, nullable=True, default=None),
        sa.Column('extra', sa.JSON, nullable=True, default=None),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    
def downgrade():
    pass
