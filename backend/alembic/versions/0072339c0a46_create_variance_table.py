"""create variance table

Revision ID: 0072339c0a46
Revises: 93dd105f671a
Create Date: 2025-01-23 13:13:26.815054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0072339c0a46'
down_revision: str = '93dd105f671a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'variance',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'product_id',
            sa.Integer,
            sa.ForeignKey('product.id', ondelete='CASCADE'),  # Explicit foreign key
            nullable=False
        ),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('variance_type', sa.String(50), nullable=False),
    )
    pass


def downgrade():
    op.drop_table('variance')
    pass
