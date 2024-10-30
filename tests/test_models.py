from app.models import User, SensorData

def test_user_model(db_session):
    # Create a user instance
    user = User(username="testuser", email="testuser@example.com")
    db_session.add(user)
    db_session.commit()
    
    # Query and check
    user_in_db = db_session.query(User).filter_by(username="testuser").first()
    assert user_in_db is not None
    assert user_in_db.username == "testuser"
    assert user_in_db.email == "testuser@example.com"

def test_sensordata_model(db_session):
    # First, create a user to link to SensorData
    user = User(username="sensoruser", email="sensoruser@example.com")
    db_session.add(user)
    db_session.commit()
    
    # Create a SensorData instance linked to the user
    sensor_data = SensorData(appId="app123", data="sensor data", messageType="info", ts=123456789, user_id=user.id)
    db_session.add(sensor_data)
    db_session.commit()
    
    # Query and check
    sensor_in_db = db_session.query(SensorData).filter_by(appId="app123").first()
    assert sensor_in_db is not None
    assert sensor_in_db.appId == "app123"
    assert sensor_in_db.user_id == user.id
    assert sensor_in_db.user == user
