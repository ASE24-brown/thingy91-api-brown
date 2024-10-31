import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.extensions import engine, init_db, reset_db, SessionLocal
from app.models import User

@pytest_asyncio.fixture(scope="module")
async def setup_database():
    """Initialize the database for testing."""
    await init_db()
    yield
    await reset_db()

@pytest_asyncio.fixture
async def async_session():
    """Provide an async session for testing."""
    async with SessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_init_db(setup_database, async_session: AsyncSession):
    """Test that init_db correctly creates tables."""
    new_user = User(username="testuser", email="testuser@example.com")
    async_session.add(new_user)
    await async_session.commit()

    # Query and check if user is in the database
    stmt = select(User).where(User.username == "testuser")
    result = await async_session.execute(stmt)
    user_in_db = result.scalars().first()

    assert user_in_db is not None
    assert user_in_db.username == "testuser"
    assert user_in_db.email == "testuser@example.com"

@pytest.mark.asyncio
async def test_reset_db(setup_database, async_session: AsyncSession):
    """Test that reset_db drops and recreates tables."""
    # Add an entry to the User table
    new_user = User(username="todelete", email="todelete@example.com")
    async_session.add(new_user)
    await async_session.commit()
    
    # Now reset the database
    await reset_db()
    
    # Check that the table is empty
    stmt = select(User)
    result = await async_session.execute(stmt)
    users = result.scalars().all()

    assert len(users) == 0
