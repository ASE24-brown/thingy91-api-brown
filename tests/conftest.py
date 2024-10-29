import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.extensions import Base
from app.models import User, SensorData

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)  # Create tables
    yield engine
    Base.metadata.drop_all(bind=engine)  # Clean up

@pytest.fixture(scope="function")
def db_session(test_engine):
    """Creates a new database session for a test."""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = Session()
    yield session
    session.close()
