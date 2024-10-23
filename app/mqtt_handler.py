import paho.mqtt.client as mqtt
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.models import SensorData, User
import asyncio
import hashlib

MQTT_BROKER = "163.172.151.151"
MQTT_PORT = 1890
MQTT_USERNAME = "brown"
MQTT_PASSWORD = "DLMJgx9NVX"

def on_connect(client, userdata, flags, rc):
    """
    Callback function for when the client receives a CONNACK response from the server.
    
    """
    if rc == 0:
        print("Connected successfully")
        client.subscribe("things/+/shadow/update")
    else:
        print(f"Failed to connect, return code {rc}")

def generate_user_id(user_id_str: str) -> int:
    """
    Generate a unique integer ID from a string using a hash function.
    """
    return int(hashlib.sha256(user_id_str.encode()).hexdigest(), 16) % (10 ** 8)

async def insert_data(session: AsyncSession, data: dict, user_id: int):
    """
    Insert sensor data into the database.
    """

    try:
        # Ensure the user exists
        user = await session.get(User, user_id)
        if not user:
            user = User(id=user_id, username=str(user_id), email=f"{user_id}@example.com")
            session.add(user)
            await session.commit()

        sensor_data = SensorData(
            appId=data['appId'],
            data=data['data'],
            messageType=data['messageType'],
            ts=int(data['ts']),
            user_id=user_id  # user_id is the foreign key
        )
        session.add(sensor_data)
        await session.commit()
    except ValueError as e:
        print(f"Error inserting data: {e}")

async def retrieve_data(session: AsyncSession):
    """
    Retrieve all sensor data from the database.
    """
    async with session:
        result = await session.execute(text("SELECT * FROM sensordata"))
        return result.fetchall()

def on_message(client, userdata, msg):
    """
    Callback function for when a PUBLISH message is received from the server.
    """
    print(f"Received message: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    session: AsyncSession = userdata['db']()

    # Extract user_id from the topic
    topic_parts = msg.topic.split('/')
    user_id_str = topic_parts[1]  # Assuming the topic format is 'things/{user_id}/shadow/update'
    user_id = generate_user_id(user_id_str)
    
    asyncio.run(insert_data(session, data, user_id))

def start_mqtt_listener(app):
    """
    Start the MQTT listener.
    """

    client = mqtt.Client(userdata={'db': app['db']})
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()