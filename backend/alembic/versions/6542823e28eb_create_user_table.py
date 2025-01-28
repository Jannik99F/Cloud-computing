"""create user table

Revision ID: 6542823e28eb
Revises: 
Create Date: 2025-01-09 18:12:04.340999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6542823e28eb'
down_revision: Union[str, None] = '0072339c0a46'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('password', sa.String(50), nullable=False),
        sa.Column('address', sa.String(50), nullable=False),
    )
    pass

def downgrade():
    op.drop_table('user')
    pass
