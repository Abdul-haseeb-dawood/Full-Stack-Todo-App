from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine('postgresql+asyncpg://neondb_owner:npg_Vi0MAbn1SrQe@ep-snowy-cherry-ah8bfctf-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require', echo=True)
