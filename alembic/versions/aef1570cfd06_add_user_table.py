"""Add user table

Revision ID: aef1570cfd06
Revises: 8f68d5236faf
Create Date: 2022-06-17 10:16:05.499058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aef1570cfd06'
down_revision = '8f68d5236faf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(),nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass
