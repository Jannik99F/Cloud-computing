"""add_image_url_to_product

Revision ID: add_image_url_to_product
Revises: 87bcedf3a9ab
Create Date: 2025-02-28

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_image_url_to_product'
down_revision = '87bcedf3a9ab'
branch_labels = None
depends_on = None


def upgrade():
    # Execute raw SQL to add the image_url column
    op.execute("""
    ALTER TABLE product 
    ADD COLUMN image_url VARCHAR NULL;
    """)


def downgrade():
    # Execute raw SQL to drop the image_url column
    op.execute("""
    ALTER TABLE product 
    DROP COLUMN image_url;
    """)