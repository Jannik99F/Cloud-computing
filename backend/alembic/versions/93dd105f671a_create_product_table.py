"""create product table

Revision ID: 93dd105f671a
Revises:
Create Date: 2025-01-23 13:04:43.070117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '93dd105f671a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('base_price', sa.Float, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('furniture_type', sa.String(50), nullable=False),
        sa.Column('product_type', sa.String(50), nullable=False),
        sa.Column('height', sa.Float, nullable=False),
        sa.Column('width', sa.Float, nullable=False),
        sa.Column('depth', sa.Float, nullable=False),
    )
    pass


def downgrade():
    op.drop_table('product')
    pass
