"""create posts table

Revision ID: 7684e2d96011
Revises: 
Create Date: 2026-10-04 01:14:19.197956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7684e2d96011'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = False),
                    sa.Column('title', sa.String, nullable = False))
    



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')
    pass
