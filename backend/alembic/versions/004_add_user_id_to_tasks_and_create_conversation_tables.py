"""Add user_id to tasks and create conversations/messages tables

Revision ID: 004_add_user_id_to_tasks_and_create_conversation_tables
Revises: 003_add_users_table
Create Date: 2026-01-18 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision: str = '004_add_user_id_to_tasks_and_create_conversation_tables'
down_revision: Union[str, None] = '003_add_users_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add user_id column to tasks table
    op.add_column('tasks', sa.Column('user_id', sa.String(255), nullable=True))
    
    # Update existing tasks to have a default user_id (for demo purposes)
    # In a real application, you would handle this differently
    # op.execute("UPDATE tasks SET user_id = 'default_user' WHERE user_id IS NULL")
    
    # Make user_id non-nullable after populating
    # op.alter_column('tasks', 'user_id', nullable=False)
    
    # Create index on user_id for faster queries
    op.create_index(op.f('ix_tasks_user_id'), 'tasks', ['user_id'], unique=False)
    
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index on user_id for conversations
    op.create_index(op.f('ix_conversations_user_id'), 'conversations', ['user_id'], unique=False)
    
    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('conversation_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),  # 'user' or 'assistant'
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                  onupdate=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], )
    )
    
    # Create indexes for messages
    op.create_index(op.f('ix_messages_user_id'), 'messages', ['user_id'], unique=False)
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_messages_role'), 'messages', ['role'], unique=False)


def downgrade() -> None:
    # Drop indexes for messages
    op.drop_index(op.f('ix_messages_role'), table_name='messages')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_user_id'), table_name='messages')
    
    # Drop messages table
    op.drop_table('messages')
    
    # Drop indexes for conversations
    op.drop_index(op.f('ix_conversations_user_id'), table_name='conversations')
    
    # Drop conversations table
    op.drop_table('conversations')
    
    # Drop index on user_id for tasks
    op.drop_index(op.f('ix_tasks_user_id'), table_name='tasks')
    
    # Drop user_id column from tasks
    op.drop_column('tasks', 'user_id')