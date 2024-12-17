from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = 'sqlite+aiosqlite:///./thingy91.db'

DATABASE_URL = 'sqlite+aiosqlite:///./data/thingy91.db'

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession,expire_on_commit=False)
Base = declarative_base()

async def init_db():
    """
    Initialize the database

    Returns: 
        None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def reset_db():
    """
    Drop and recreate the database

    Returns: 
        None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def setup_db(app):
    """
    Setup the database for the aiohttp application

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Returns:
        None
    """
    await init_db()
    app['db'] = SessionLocal