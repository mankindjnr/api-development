"""create posts table

Revision ID: 6dc49806a1ba
Revises: 
Create Date: 2023-11-08 15:45:54.264652

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6dc49806a1ba'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
     sa.Column('title', sa.String(length=255), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
