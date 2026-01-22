from sqlalchemy import create_engine, text
from app.core.settings import settings

# Create a sync engine to connect to the database
sync_url = settings.database_url.replace('postgresql+asyncpg://neondb_owner:npg_Vi0MAbn1SrQe@ep-snowy-cherry-ah8bfctf-pooler.c-3.us-east-1.aws.neon.tech/neondb')
engine = create_engine(sync_url)

# Add the user_id column to the tasks table if it doesn't exist
with engine.connect() as conn:
    # Check if user_id column exists
    result = conn.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'tasks' AND column_name = 'user_id'
    """))
    
    if result.fetchone() is None:
        # Add the user_id column
        conn.execute(text("ALTER TABLE tasks ADD COLUMN user_id VARCHAR(255)"))
        conn.execute(text("CREATE INDEX ix_tasks_user_id ON tasks (user_id)"))
        conn.commit()
        print("Added user_id column to tasks table")
    else:
        print("user_id column already exists in tasks table")

    # Verify the column exists now
    result = conn.execute(text("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'tasks' AND column_name = 'user_id'
    """))
    row = result.fetchone()
    if row:
        print(f"Verified: {row[0]} column exists with type {row[1]}")
    else:
        print("ERROR: user_id column still doesn't exist!")