"""create table inventory

Revision ID: 87bcedf3a9ab
Revises: 3d0481fff148
Create Date: 2025-02-03 15:31:21.477842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87bcedf3a9ab'
down_revision: Union[str, None] = '3d0481fff148'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    op.create_table(
        'inventory',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column(
            'variance_id',
            sa.Integer,
            sa.ForeignKey('variance.id', ondelete='CASCADE'),
            nullable=False,
        ),
        sa.Column('amount', sa.Integer),
    )
    op.create_unique_constraint('uq_variance_id', 'inventory', ['variance_id'])

def downgrade():
    op.drop_table('inventory')
    pass
