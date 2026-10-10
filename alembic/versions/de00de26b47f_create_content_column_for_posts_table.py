"""create content column for posts table

Revision ID: de00de26b47f
Revises: 7684e2d96011
Create Date: 2026-10-04 01:46:25.740440

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de00de26b47f'
down_revision: Union[str, Sequence[str], None] = '7684e2d96011'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable =False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
