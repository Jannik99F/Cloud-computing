"""add basket item table

Revision ID: 19f1e3d1fd11
Revises: 4d771dbeeebb
Create Date: 2025-01-28 15:45:22.890050

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19f1e3d1fd11'
down_revision: Union[str, None] = '4d771dbeeebb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'basket_item',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'basket_id',
            sa.Integer,
            sa.ForeignKey('basket.id', ondelete='CASCADE'),
            nullable=False
        ),
        sa.Column(
            'variance_id',
            sa.Integer,
            sa.ForeignKey('variance.id', ondelete='CASCADE'),
            nullable=False
        ),
        sa.Column('amount', sa.Integer),
        sa.Column('base_price', sa.Float, nullable=True),
        sa.Column('variance_price', sa.Float, nullable=True),
    )
    pass


def downgrade():
    op.drop_table('basket_item')
    pass
