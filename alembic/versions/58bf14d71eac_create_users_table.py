"""create users table

Revision ID: 58bf14d71eac
Revises: 13adb6e6c840
Create Date: 2023-11-08 16:05:26.463409

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '58bf14d71eac'
down_revision: Union[str, None] = '13adb6e6c840'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('password', sa.String(255), nullable=False),
        sa.Column('create_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
        )


def downgrade() -> None:
    op.drop_table('users')
    pass
