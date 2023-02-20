"""add users_count

Revision ID: 3b9252b28f45
Revises: 0cdc72413cb6
Create Date: 2023-02-20 18:07:34.566741

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3b9252b28f45'
down_revision = '0cdc72413cb6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users_activity',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('user_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_activity_id'), 'users_activity', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_activity_id'), table_name='users_activity')
    op.drop_table('users_activity')
    # ### end Alembic commands ###
