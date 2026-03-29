"""add server_default for is_active

Revision ID: 672c4d29c4a9
Revises: 0f6e1557778b
Create Date: 2026-03-29 16:27:15.537793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '672c4d29c4a9'
down_revision: Union[str, Sequence[str], None] = '0f6e1557778b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('students', 'is_active',
                    server_default=sa.text('true'))


def downgrade() -> None:
    op.alter_column('students', 'is_active',
                    server_default=None)
