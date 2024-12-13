import paho.mqtt.client as mqtt
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from app.models import SensorData, User, Device
from app.extensions import SessionLocal
import asyncio
import hashlib
import datetime
from datetime import datetime
import logging
import re

MQTT_BROKER = "163.172.151.151"
MQTT_PORT = 1890
MQTT_USERNAME = "brown"
MQTT_PASSWORD = "DLMJgx9NVX"

def on_connect(client, userdata, flags, rc):
    """
    Callback function for when the client receives a CONNACK response from the server.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (dict): The private user data as set in Client() or userdata_set().
        flags (dict): Response flags sent by the broker.
        rc (int): The connection result.

    Returns:
        None
    """
    if rc == 0:
        print("Connected successfully")
        client.subscribe("things/+/shadow/update")
    else:
        print(f"Failed to connect, return code {rc}")

def generate_user_id(user_id_str: str) -> int:
    """
    Generate a unique integer ID from a string using a hash function.

    Args:
        user_id_str (str): The user ID string.

    Returns:
        int: The generated unique integer ID.
    """
    return int(hashlib.sha256(user_id_str.encode()).hexdigest(), 16) % (10 ** 8)


async def insert_data(session: AsyncSession, data: dict, device_id: str):
    """
    Insert sensor data into the database.

    Args:
        session (AsyncSession): The database session.
        data (dict): The sensor data to insert.
        device_id (str): The device ID associated with the sensor data.

    Returns:
        None
    """
    try:
        # Extract the integer part from the device_id
        match = re.search(r'\d+', device_id)
        if not match:
            logging.error("Error: Device ID does not contain an integer.")
            return
        device_number = int(match.group())

        # Ensure the user exists
        await session.begin()
        user = await session.get(User, device_number)
        if not user:
            user = User(id=device_number, username=str(device_number), email=f"{device_number}@example.com")
            logging.debug("Inserting new user...")
            session.add(user)
            await session.commit()
            logging.debug("User inserted.")
        else:
            await session.commit()  # Commit if user already exists

        # Validate that the necessary data fields are present
        appId = data.get('appId')
        data_field = data.get('data', {})
        messageType = data.get('messageType')
        ts = data.get('ts', 0)

        # Ensure appId and messageType exist before creating SensorData
        if appId is None or messageType is None:
            logging.error("Error: Missing 'appId' or 'messageType' in the data payload.")
            return  # Exit the function if required fields are missing

        # Create and insert sensor data
        sensor_data = SensorData(
            appId=appId,
            data=data_field,
            messageType=messageType,
            ts=int(ts),
            user_id=device_number,
            device_id=device_id
        )

        logging.debug("Inserting sensor data...")
        session.add(sensor_data)
        # Update device status and last_updated
        device = await session.get(Device, device_number)
        if device:
            device.status = 1
            device.last_updated = datetime.now()
            session.add(device)
        else:
            logging.debug(f"Device with ID {device_number} not found. Creating new device entry.")
            new_device = Device(
                id=device_number,
                name=f"brown-{device_number}",  # Set the name as brown-{device_number}
                user_id=device_number,
                status=1,
                last_updated=datetime.now()
            )
            logging.debug(f"New device details: {new_device}")
            session.add(new_device)

        await session.commit()
        logging.debug("Data inserted.")
    except ValueError as e:
        logging.error(f"Error inserting data: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        # Ensure session is closed outside the async context if not done already
        await session.close()

async def retrieve_data(session: AsyncSession):
    """
    Retrieve all sensor data from the database.

    Args:
        session (AsyncSession): The database session.

    Returns:
        list: A list of all sensor data.
    """
    async with session:
        result = await session.execute(text("SELECT * FROM sensordata"))
        return result.fetchall()
    
async def create_user_with_profile(username, email, name, description, type):
    """
    Create a new user with a profile.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        name (str): The name of the profile.
        description (str): The description of the profile.
        type (str): The type of the profile.

    Returns:
        None
    """
    async with SessionLocal() as session:
        async with session.begin():
            user = User(username=username, email=email)
            session.add(user)
            await session.flush()

            profile = Profile(name=name, description=description, type=type, user_id=user.id)
            session.add(profile)
            await session.commit()

async def retrieve_user_with_profile():
    """
    Retrieve all user profiles from the database.

    Returns:
        list: A list of all user profiles.
    """
    async with SessionLocal() as session:
        async with session:
            result = await session.execute(text("SELECT * FROM user_profile"))
            return result.fetchall()

def on_message(client, userdata, msg):
    """
    Callback function for when a PUBLISH message is received from the server.

    Args:
        client (mqtt.Client): The MQTT client instance.
        userdata (dict): The private user data as set in Client() or userdata_set().
        msg (mqtt.MQTTMessage): An instance of MQTTMessage, which contains topic and payload.

    Returns:
        None
    """
    print(f"Received message: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    session: AsyncSession = userdata['db']()

    # Extract user_id from the topic
    topic_parts = msg.topic.split('/')
    device_id = topic_parts[1]  # Assuming the topic format is 'things/{device_id}/shadow/update'
    
    asyncio.run(insert_data(session, data, device_id))

def start_mqtt_listener(app):
    """
    Start the MQTT listener.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Returns:
        None
    """
    client = mqtt.Client(userdata={'db': app['db']})
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()