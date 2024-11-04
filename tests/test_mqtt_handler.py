import pytest
import json
from unittest.mock import AsyncMock, MagicMock
from app.mqtt_handler import on_connect, on_message, insert_data, generate_user_id
from app.models import SensorData, User
from sqlalchemy.sql import text

# Sample test data
sample_payload = {
    "appId": "app123",
    "data": "some_sensor_data",
    "messageType": "update",
    "ts": 1690587600
}

# Sample MQTT topic
sample_topic = "things/uniqueUser123/shadow/update"

@pytest.fixture
def mock_session():
    """Fixture to provide a mock database session."""
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    session.commit = AsyncMock()
    session.add = AsyncMock()
    return session



def test_generate_user_id():
    """Test the generate_user_id function."""
    user_id = generate_user_id("uniqueUser123")
    assert isinstance(user_id, int)
    assert user_id < 10**8  # Ensures it stays within 8 digits

@pytest.mark.asyncio
async def test_insert_data(mocker, mock_session):
    """Test inserting sensor data into the database."""
    mock_session = AsyncMock()
    user_id = generate_user_id("uniqueUser123")
    await insert_data(mock_session, sample_payload, user_id)

    # Check if user and sensor data were added
    mock_session.add.assert_awaited()  # Ensure user or sensor data was added
    mock_session.commit.assert_awaited()  # Ensure a commit was called

def test_on_connect(mocker):
    """Test the on_connect callback."""
    client = MagicMock()
    on_connect(client, None, None, 0)
    client.subscribe.assert_called_with("things/+/shadow/update")

def test_on_message(mocker, mock_session):
    """Test the on_message callback."""
    # Mock MQTT client and setup
    client = MagicMock()
    client.user_data_set({'db': lambda: mock_session})

    # Create a mock message
    mock_msg = MagicMock()
    mock_msg.payload = json.dumps(sample_payload).encode('utf-8')
    mock_msg.topic = sample_topic

    # Test on_message
    mocker.patch("app.mqtt_handler.insert_data", new=AsyncMock())
    on_message(client, client._userdata, mock_msg)
    
    app_id = sample_payload['appId']
    data = sample_payload['data']
    
    # Check that the message handling logic was executed with the correct data
    app_id
