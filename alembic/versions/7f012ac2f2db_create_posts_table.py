"""create posts table

Revision ID: 7f012ac2f2db
Revises: 
Create Date: 2022-06-17 09:53:55.582587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f012ac2f2db'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
    sa.Column('id', sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
