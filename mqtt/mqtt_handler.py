import paho.mqtt.client as mqtt
import json
import asyncio
import logging
import re
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import SensorData, User, Device
from datetime import datetime

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

async def insert_data(session: AsyncSession, data: dict, device_id: str):
    """
    Insert sensor data into the database and ensure proper associations between users and devices.

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

        await session.begin()

        # Check if the device exists
        device = await session.get(Device, device_number)
        if not device:
            # If the device does not exist, create it with an associated user
            logging.debug(f"Device with ID {device_number} not found. Creating new device entry.")
            user = await session.get(User, device_number)
            if not user:
                user = User(id=device_number, username=str(device_number), email=f"{device_number}@example.com")
                session.add(user)

            new_device = Device(
                id=device_number,
                name=f"brown-{device_number}",  # Set the name as brown-{device_number}
                user_id=user.id,
                status=1,
                last_updated=datetime.now()
            )
            session.add(new_device)
            device = new_device
        else:
            # If the device exists, ensure it has the correct user association
            user = await session.get(User, device.user_id)
            if not user:
                logging.error(f"Device {device_number} exists but has no associated user.")
                return

        # Validate that the necessary data fields are present
        appId = data.get('appId')
        data_field = data.get('data', {})
        messageType = data.get('messageType')
        ts = data.get('ts', 0)

        if appId is None or messageType is None:
            logging.error("Error: Missing 'appId' or 'messageType' in the data payload.")
            return  # Exit if required fields are missing

        # Create and insert sensor data
        sensor_data = SensorData(
            appId=appId,
            data=data_field,
            messageType=messageType,
            ts=int(ts),
            user_id=device.user_id,
            device_id=device.id
        )

        logging.debug("Inserting sensor data...")
        session.add(sensor_data)

        # Update device status and last_updated
        device.status = 1
        device.last_updated = datetime.now()
        session.add(device)

        await session.commit()
        logging.debug("Data successfully inserted.")
    except ValueError as e:
        logging.error(f"Error inserting data: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    finally:
        # Ensure session is closed
        await session.close()

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