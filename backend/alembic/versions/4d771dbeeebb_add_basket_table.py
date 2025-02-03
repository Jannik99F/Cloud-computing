"""add basket table

Revision ID: 4d771dbeeebb
Revises: 6542823e28eb
Create Date: 2025-01-28 14:51:59.359240

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d771dbeeebb'
down_revision: Union[str, None] = '6542823e28eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'basket',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'user_id',
            sa.Integer,
            sa.ForeignKey('product.id', ondelete='CASCADE'),
            nullable=False
        ),
    )
    pass

def downgrade():
    op.drop_table('basket')
    pass
