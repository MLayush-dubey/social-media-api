"""add content column to posts table

Revision ID: 91d6134509f3
Revises: 0114db9ea63e
Create Date: 2025-11-28 14:37:01.314720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91d6134509f3'
down_revision: Union[str, Sequence[str], None] = '0114db9ea63e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
