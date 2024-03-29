"""chenged model entry in vehicle db to nullable

Revision ID: f079976e0d97
Revises: vehicle_brand_nullable
Create Date: 2023-01-23 03:45:59.666462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f079976e0d97'
down_revision = 'vehicle_brand_nullable'
branch_labels = ('vehicle.model_is_nullable',)
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vehicles', 'model',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vehicles', 'model',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
