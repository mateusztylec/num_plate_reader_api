"""Base vehicle table

Revision ID: 72c2d1e00233
Revises: 
Create Date: 2022-08-17 22:33:01.327587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c2d1e00233'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vehicles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('num_plate', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vehicles')
    # ### end Alembic commands ###
