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
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'variance',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('product_id', sa.Integer),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('variance_type', sa.String(50), nullable=False),
    )

    op.create_foreign_key(
        constraint_name="fk_product_variance",
        source_table="variance",
        referent_table="product",
        local_cols=["product_id"],
        remote_cols=["id"]
    )
    pass


def downgrade():
    op.drop_table('variance')
    pass
