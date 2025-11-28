"""create posts table

Revision ID: 0114db9ea63e
Revises: 
Create Date: 2025-11-28 14:05:08.961575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0114db9ea63e'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#upgrade schema
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),  #creating posts table
                     sa.Column('title', sa.String(), nullable=False))
    pass

#downgrade schema
def downgrade() -> None:
    op.drop_table('posts')
    pass
