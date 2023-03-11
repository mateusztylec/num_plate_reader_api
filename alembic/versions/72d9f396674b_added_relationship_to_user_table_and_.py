"""added relationship to user table and nullable to role

Revision ID: 72d9f396674b
Revises: 9ec88d1e714f
Create Date: 2023-03-11 22:19:47.477423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72d9f396674b'
down_revision = '9ec88d1e714f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
