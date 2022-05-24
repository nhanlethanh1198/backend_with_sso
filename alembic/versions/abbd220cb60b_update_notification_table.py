"""update notification table

Revision ID: abbd220cb60b
Revises: c79cb4c386b5
Create Date: 2022-01-25 23:27:06.157123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'abbd220cb60b'
down_revision = 'c79cb4c386b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('system_notification', sa.Column('image', sa.String(length=255), nullable=True))
    op.add_column('user_and_staff_notification', sa.Column('image', sa.String(length=255), nullable=True))
    op.add_column('system_notification', sa.Column('staff_id', sa.Integer, nullable=False))
    op.add_column('user_and_staff_notification', sa.Column('staff_id', sa.Integer, nullable=False))

    op.create_foreign_key('fk_system_notification_staff_id', 'system_notification', 'staffs', ['staff_id'], ['id'])
    op.create_foreign_key('fk_user_and_staff_notification_staff_id', 'user_and_staff_notification', 'staffs', ['staff_id'], ['id'])


def downgrade():
    op.drop_constraint('fk_user_and_staff_notification_staff_id', 'user_and_staff_notification', type_='foreignkey')
    op.drop_constraint('fk_system_notification_staff_id', 'system_notification', type_='foreignkey')
    op.drop_column('user_and_staff_notification', 'staff_id')
    op.drop_column('system_notification', 'staff_id')
    op.drop_column('user_and_staff_notification', 'image')
    op.drop_column('system_notification', 'image')
