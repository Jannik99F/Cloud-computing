"""add order table

Revision ID: 3d0481fff148
Revises: 19f1e3d1fd11
Create Date: 2025-01-29 14:06:26.891352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d0481fff148'
down_revision: Union[str, None] = '19f1e3d1fd11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('payment_secret', sa.String(), nullable=True),
        sa.Column('shipping_address', sa.String(), nullable=True),
        sa.Column('billing_address', sa.String(), nullable=True),
        sa.Column('payment_method', sa.String(), nullable=True),
        sa.Column('payed', sa.Boolean(), nullable=False),
        sa.Column('items_reserved', sa.Boolean(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column(
            'basket_id',
            sa.Integer,
            sa.ForeignKey('basket.id', ondelete='CASCADE'),
            nullable=False
        ),
    )
    pass

def downgrade():
    op.drop_table('order')
    pass
