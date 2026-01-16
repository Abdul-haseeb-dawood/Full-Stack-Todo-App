"""Add priority column to tasks table

Revision ID: 002_add_priority_column
Revises: 001_initial_task_table
Create Date: 2026-01-15 14:45:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '002_add_priority_column'
down_revision: Union[str, None] = '001_initial_task_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add priority column to tasks table with default value 'medium'
    op.add_column('tasks', sa.Column('priority', sa.String(20), nullable=False, server_default='medium'))


def downgrade() -> None:
    # Remove priority column from tasks table
    op.drop_column('tasks', 'priority')