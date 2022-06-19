"""Add foreign key to posts table

Revision ID: da8e68d81867
Revises: aef1570cfd06
Create Date: 2022-06-17 10:23:58.779458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da8e68d81867'
down_revision = 'aef1570cfd06'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users__fk', source_table='posts', referent_table='users',
                            local_cols=['owner_id'], remote_cols= ['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
