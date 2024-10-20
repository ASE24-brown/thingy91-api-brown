import paho.mqtt.client as mqtt
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from .models import SensorData
import asyncio

MQTT_BROKER = "163.172.151.151"
MQTT_PORT = 1890
MQTT_USERNAME = "brown"
MQTT_PASSWORD = "DLMJgx9NVX"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("things/brown-3/shadow/update")
    else:
        print(f"Failed to connect, return code {rc}")

async def insert_data(session: AsyncSession, data: dict):
    try:
        sensor_data = SensorData(
            appId=data['appId'],
            data=float(data['data']),
            messageType=data['messageType'],
            ts=int(data['ts'])
        )
        session.add(sensor_data)
        await session.commit()
    except ValueError as e:
        print(f"Error inserting data: {e}")

async def retrieve_data(session: AsyncSession):
    async with session:
        result = await session.execute(text("SELECT * FROM sensor_data"))
        return result.fetchall()

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()}")
    data = json.loads(msg.payload.decode())
    session: AsyncSession = userdata['db']()
    asyncio.run(insert_data(session, data))

def start_mqtt_listener(app):
    client = mqtt.Client(userdata={'db': app['db']})
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()