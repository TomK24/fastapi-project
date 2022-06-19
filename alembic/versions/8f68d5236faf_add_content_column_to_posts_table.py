"""add content column to posts table

Revision ID: 8f68d5236faf
Revises: 7f012ac2f2db
Create Date: 2022-06-17 10:11:29.585474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f68d5236faf'
down_revision = '7f012ac2f2db'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
