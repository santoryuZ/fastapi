"""add foreign key to posts table

Revision ID: 0c59cf2e8fc6
Revises: aa7c27b5b775
Create Date: 2026-10-04 02:00:06.616953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c59cf2e8fc6'
down_revision: Union[str, Sequence[str], None] = 'aa7c27b5b775'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_users_fk', source_table= 'posts', referent_table= 'users', local_cols=['owner_id'], remote_cols=['id'], ondelete = 'CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk', table_name= 'posts')
    op.drop_column('posts', 'owner_id')
