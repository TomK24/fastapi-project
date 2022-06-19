"""Add remaining columns to posts table

Revision ID: 483b5763231b
Revises: da8e68d81867
Create Date: 2022-06-17 11:07:54.023324

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483b5763231b'
down_revision = 'da8e68d81867'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
