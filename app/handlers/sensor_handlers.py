from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal


async def list_sensor_data(request):
    """
    ---
    summary: Retrieve a list of all sensor data
    description: Retrieves a list of all sensor data from the database.
    tags:
      - SensorData
    responses:
      '200':
        description: A list of sensor data
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  appId:
                    type: string
                  data:
                    type: string
                  messageType:
                    type: string
                  timestamp:
                    type: string
                    format: date-time
                  user_id:
                    type: integer
    """
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(SensorData))
            sensor_data = result.scalars().all()
            return web.json_response([{
                "id": sensor.id,
                "appId": sensor.appId,
                "data": sensor.data,
                "messageType": sensor.messageType,
                "timestamp": sensor.ts,
                "user_id": sensor.user_id
            } for sensor in sensor_data])

async def clear_sensor_data(request):
    """
    ---
    summary: Delete all sensor data
    description: Deletes all sensor data from the database.
    tags:
      - SensorData
    responses:
      '204':
        description: Sensor data deleted successfully
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(SensorData))
            await session.commit()
            return web.Response(status=204)

async def add_sensor_data(request):
    """
    ---
    summary: Create new sensor data
    description: Creates new sensor data in the database.
    tags:
      - SensorData
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              user_id:
                type: integer
                description: ID of the user associated with the sensor data
              appId:
                type: string
                description: Application ID
              data:
                type: string
                description: Sensor data
              messageType:
                type: string
                description: Type of the message
              ts:
                type: string
                format: date-time
                description: Timestamp of the sensor data
    responses:
      '201':
        description: Sensor data created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                appId:
                  type: string
                data:
                  type: string
                messageType:
                  type: string
                timestamp:
                  type: string
                  format: date-time
                user_id:
                  type: integer
      '500':
        description: Failed to add sensor data
    """
    data = await request.json()
    user_id = data.get('user_id')  # user_id is now optional
    appId = data.get('appId')
    sensor_data = data.get('data')
    messageType = data.get('messageType')
    ts = data.get('ts')

    async with SessionLocal() as session:
        #async with session.begin():
            try:
                # Create sensor data without requiring a user
                sensordata = SensorData(
                    user_id=user_id,
                    appId=appId,
                    data=sensor_data,
                    messageType=messageType,
                    ts=ts
                )
                session.add(sensordata)
                await session.commit()
                await session.refresh(sensordata)
                return web.json_response({
                    "id": sensordata.id,
                    "appId": sensordata.appId,
                    "data": sensordata.data,
                    "messageType": sensordata.messageType,
                    "timestamp": sensordata.ts,
                    "user_id": sensordata.user_id
                }, status=201)
            except IntegrityError:
                await session.rollback()
                return web.json_response({"error": "Failed to add sensor data"}, status=500)

async def show_sensor_data(request):
    """
    ---
    summary: Retrieve specific sensor data by ID
    description: Retrieves specific sensor data from the database by its ID.
    tags:
      - SensorData
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '200':
        description: A sensor data object
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                appId:
                  type: string
                data:
                  type: string
                messageType:
                  type: string
                timestamp:
                  type: string
                  format: date-time
                user_id:
                  type: integer
      '404':
        description: Sensor data not found
    """
    sensor_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            sensor = await session.get(SensorData, sensor_id)
            if not sensor:
                raise web.HTTPNotFound(reason='Sensor data not found')
            return web.json_response({
                "id": sensor.id,
                "appId": sensor.appId,
                "data": sensor.data,
                "messageType": sensor.messageType,
                "timestamp": sensor.ts,
                "user_id": sensor.user_id
            })

async def update_sensor_data(request):
    """
    ---
    summary: Update specific sensor data by ID
    description: Updates specific sensor data in the database by its ID.
    tags:
      - SensorData
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              appId:
                type: string
              data:
                type: string
              messageType:
                type: string
              timestamp:
                type: string
                format: date-time
              user_id:
                type: integer
    responses:
      '200':
        description: Sensor data updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                appId:
                  type: string
                data:
                  type: string
                messageType:
                  type: string
                timestamp:
                  type: string
                  format: date-time
                user_id:
                  type: integer
      '404':
        description: Sensor data not found
    """
    sensor_id = request.match_info['id']
    data = await request.json()
    async with SessionLocal() as session:
        sensor = await session.get(SensorData, sensor_id)
        if not sensor:
            raise web.HTTPNotFound(reason='Sensor data not found')
        for key, value in data.items():
            setattr(sensor, key, value)
        await session.commit()
        await session.refresh(sensor)
        return web.json_response({
            "id": sensor.id,
            "appId": sensor.appId,
            "data": sensor.data,
            "messageType": sensor.messageType,
            "timestamp": sensor.ts,
            "user_id": sensor.user_id
        })

async def remove_sensor_data(request):
    """
    ---
    summary: Delete specific sensor data by ID
    description: Deletes specific sensor data from the database by its ID.
    tags:
      - SensorData
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '204':
        description: Sensor data deleted successfully
      '404':
        description: Sensor data not found
    """
    sensor_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            sensor = await session.get(SensorData, sensor_id)
            if not sensor:
                raise web.HTTPNotFound(reason='Sensor data not found')
            await session.delete(sensor)
            await session.commit()
            return web.Response(status=204)
        
async def get_sensor_data(request):
    """
    ---
    summary: Retrieve all sensor data
    description: Retrieves all sensor data from the database.
    tags:
      - SensorData
    responses:
      '200':
        description: A list of sensor data
        content:
          application/json:
            schema:
              type: object
              properties:
                sensor_data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      appId:
                        type: string
                      data:
                        type: string
                      messageType:
                        type: string
                      timestamp:
                        type: string
                        format: date-time
    """
    async with SessionLocal() as db:  # Use async context manager
        # Use an async query to fetch all sensor data
        result = await db.execute(select(SensorData))
        data = result.scalars().all()
        
        sensor_data = [
            {
                "id": sensor.id,
                "appId": sensor.appId,
                "data": sensor.data,
                "messageType": sensor.messageType,
                "timestamp": sensor.ts
            }
            for sensor in data
        ]
        return web.json_response({"sensor_data": sensor_data})
        
