from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from app.models import SensorData
from app.extensions import SessionLocal
from app.models import User, Device


async def list_sensor_data(request):
    """
    Retrieves a list of all sensor data from the database.
    
    params:
      request: The request object.
    return:
      A JSON response containing a list of sensor data.
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
    Deletes all sensor data from the database.
    
    params:
      request: The request object.
    return:
      A response indicating the success of the operation.
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(SensorData))
            await session.commit()
            return web.Response(status=204)

async def add_sensor_data(request):
    """
    Creates new sensor data in the database.
    
    params:
      request: The request object containing sensor data.
    return:
      A JSON response with the created sensor data or an error message.
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
    Retrieves specific sensor data from the database by its ID.
    
    params:
      request: The request object containing the sensor data ID.
    return:
      A JSON response with the sensor data details or a 404 error if the sensor data is not found.
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
    Updates specific sensor data in the database by its ID.
    
    params:
      request: The request object containing sensor data.
    return:
      A JSON response with the updated sensor data details or a 404 error if the sensor data is not found.
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
    Deletes specific sensor data from the database by its ID.
    
    params:
      request: The request object containing sensor data.
    return:
      A JSON response with the updated sensor data details or a 404 error if the sensor data is not found.
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
    Retrieves all sensor data from the database.
    
    params:
      request: The request object.
    return:
      A JSON response containing a list of sensor data.
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
        
async def get_all_sensor_data_for_user(request):
    """
    Get all sensor data for all devices belonging to a user.
    Args:
        request (web.Request): The request object containing the user ID.
    Returns:
        web.Response: A JSON response with the sensor data for the specified user.
    """
    user_id = request.match_info.get('user_id')  # Extract user_id from the request
    if not user_id:
        return web.json_response({"error": "User ID is required"}, status=400)
    async with SessionLocal() as session:
        async with session.begin():
            # Verify the user exists
            user = await session.get(User, user_id)
            if not user:
                return web.json_response({"error": "User not found"}, status=404)
            # Fetch sensor data for all devices associated with the user
            result = await session.execute(
                select(SensorData).join(Device).where(Device.user_id == user_id)
            )
            sensor_data = result.scalars().all()
            # Format the data
            data_list = [
                {"id": data.id, "data": data.data, "appID": data.appId, "ts": data.ts, "device_id": data.device_id}
                for data in sensor_data
            ]
            return web.json_response(data_list)
