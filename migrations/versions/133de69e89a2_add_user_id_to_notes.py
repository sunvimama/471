"""Add user_id to notes

Revision ID: 133de69e89a2
Revises: 5e69d2ee211f
Create Date: 2025-04-16 08:48:10.071171

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '133de69e89a2'
down_revision = '5e69d2ee211f'
branch_labels = None
depends_on = None


def upgrade():
    # Comment out the line below to prevent adding the column again
    # op.add_column('notes', sa.Column('user_id', sa.Integer(), nullable=False))
    pass


def downgrade():
    # Keep the downgrade logic if needed
    op.drop_column('notes', 'user_id')
