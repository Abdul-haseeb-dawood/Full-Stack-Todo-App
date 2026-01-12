# Data Model: Todo Application Backend

## Entity: Task

### Overview
The Task entity represents a single todo item in the application. It contains all the necessary information to track a user's tasks including title, description, completion status, and timestamps.

### Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Unique, Not Null | Globally unique identifier for the task |
| title | String | Not Null, Max Length: 255 | Brief title or summary of the task |
| description | String | Optional, Max Length: 1000 | Detailed description of the task (nullable) |
| completed | Boolean | Not Null, Default: False | Flag indicating if the task is completed |
| created_at | DateTime | Not Null, Auto-generated | Timestamp when the task was created |
| updated_at | DateTime | Not Null, Auto-generated, Updates on Change | Timestamp when the task was last updated |

### Relationships
- The Task entity is standalone with no direct relationships to other entities in the current scope
- Future extensions might include relationships to users or categories

### Validation Rules
1. **Title Validation**:
   - Required field (cannot be null or empty)
   - Must be between 1 and 255 characters
   - Cannot consist only of whitespace

2. **Description Validation**:
   - Optional field (can be null)
   - If provided, must be between 1 and 1000 characters
   - Can be an empty string

3. **Completed Validation**:
   - Must be a boolean value (true/false)
   - Defaults to false when creating a new task

4. **Timestamp Validation**:
   - created_at is automatically set when the record is created
   - updated_at is automatically updated when the record is modified
   - Both timestamps are timezone-aware

### State Transitions
- **New Task Creation**: completed = False (default)
- **Task Completion**: completed = True
- **Task Reopening**: completed = False
- **Task Modification**: updated_at timestamp is updated regardless of other field changes

### Indexes
1. **Primary Index**: id (automatically created by primary key constraint)
2. **Completion Status Index**: completed (for efficient querying of completed/incomplete tasks)
3. **Creation Time Index**: created_at (for chronological ordering and time-based queries)

### Sample Data
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete project proposal",
  "description": "Finish writing the project proposal document and send it to the manager by EOD.",
  "completed": false,
  "created_at": "2026-01-11T10:00:00Z",
  "updated_at": "2026-01-11T10:00:00Z"
}
```

### Database Schema (PostgreSQL)
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at 
    BEFORE UPDATE ON tasks 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
```

### ORM Mapping (SQLAlchemy)
```python
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), 
                       onupdate=func.now(), nullable=False)
```