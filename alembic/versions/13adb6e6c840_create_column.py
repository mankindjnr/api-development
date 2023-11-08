"""create column

Revision ID: 13adb6e6c840
Revises: 6dc49806a1ba
Create Date: 2023-11-08 16:00:47.294176

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13adb6e6c840'
down_revision: Union[str, None] = '6dc49806a1ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
