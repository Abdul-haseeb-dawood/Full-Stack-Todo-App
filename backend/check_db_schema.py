from sqlalchemy import create_engine, inspect
from app.core.settings import settings
import asyncio

# Create a sync engine to inspect the database
sync_url = settings.database_url.replace('postgresql+asyncpg://neondb_owner:npg_Vi0MAbn1SrQe@ep-snowy-cherry-ah8bfctf-pooler.c-3.us-east-1.aws.neon.tech/neondb')
engine = create_engine(sync_url)

# Get list of tables
inspector = inspect(engine)
tables = inspector.get_table_names()
print('Tables in database:')
for table in tables:
    print(f'  - {table}')

# Check columns in tasks table
if 'tasks' in tables:
    columns = inspector.get_columns('tasks')
    print('\nColumns in tasks table:')
    for col in columns:
        print(f'  - {col["name"]}: {col["type"]}')

# Check if conversations and messages tables exist
if 'conversations' in tables:
    print('\nConversations table exists')
    conv_cols = inspector.get_columns('conversations')
    for col in conv_cols:
        print(f'  - {col["name"]}: {col["type"]}')
else:
    print('\nConversations table does not exist')

if 'messages' in tables:
    print('\nMessages table exists')
    msg_cols = inspector.get_columns('messages')
    for col in msg_cols:
        print(f'  - {col["name"]}: {col["type"]}')
else:
    print('\nMessages table does not exist')

# Check alembic version table
if 'alembic_version' in tables:
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM alembic_version"))
        rows = result.fetchall()
        print('\nAlembic version table:')
        for row in rows:
            print(f'  - {row}')
else:
    print('\nAlembic version table does not exist')