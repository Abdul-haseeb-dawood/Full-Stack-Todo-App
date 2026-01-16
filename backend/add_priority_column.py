from sqlalchemy import text
from app.db.database import engine
import asyncio


async def add_priority_column():
    """Add the priority column to the tasks table if it doesn't exist."""
    async with engine.begin() as conn:
        # Check if the priority column exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'tasks' AND column_name = 'priority'
        """))
        
        if not result.fetchone():
            # Add the priority column if it doesn't exist
            await conn.execute(text("ALTER TABLE tasks ADD COLUMN priority VARCHAR(20) DEFAULT 'medium' NOT NULL"))
            await conn.commit()
            print("Priority column added successfully!")
        else:
            print("Priority column already exists.")


if __name__ == "__main__":
    asyncio.run(add_priority_column())