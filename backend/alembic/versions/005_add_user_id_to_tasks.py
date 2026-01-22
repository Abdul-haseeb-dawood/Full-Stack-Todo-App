"""Add user_id column to tasks table

Revision ID: 005_add_user_id_to_tasks
Revises: 004_add_user_id_to_tasks_and_create_conversation_tables
Create Date: 2026-01-18 15:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '005_add_user_id_to_tasks'
down_revision: Union[str, None] = '004_add_user_id_to_tasks_and_create_conversation_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column to tasks table if it doesn't exist
    # First, add as nullable
    op.add_column('tasks', sa.Column('user_id', sa.String(255), nullable=True))
    
    # Create index on user_id for faster queries
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    
    # Update existing tasks to have a default user_id (for demo purposes)
    # In a real application, you would handle this differently
    # op.execute("UPDATE tasks SET user_id = 'default_user' WHERE user_id IS NULL")
    
    # Make user_id non-nullable after populating
    # For now, keeping it nullable to avoid issues with existing data
    # op.alter_column('tasks', 'user_id', nullable=False)


def downgrade() -> None:
    # Drop index on user_id for tasks
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    
    # Drop user_id column from tasks
    op.drop_column('tasks', 'user_id')