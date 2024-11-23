from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal



def setup_sensor_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /sensor_data/: Retrieves a list of all sensor data.
        DELETE /sensor_data/: Deletes all sensor data.
        POST /sensor_data/: Adds new sensor data.
        GET /sensor_data/{id}: Retrieves specific sensor data by ID.
        PATCH /sensor_data/{id}: Updates specific sensor data by ID.
        DELETE /sensor_data/{id}: Deletes specific sensor data by ID.
    """
    
    app.router.add_get('/sensor_data/', list_sensor_data)
    app.router.add_delete('/sensor_data/', clear_sensor_data)
    app.router.add_post('/sensor_data/', add_sensor_data)
    app.router.add_get('/sensor_data/{id}', show_sensor_data)
    app.router.add_patch('/sensor_data/{id}', update_sensor_data)
    app.router.add_delete('/sensor_data/{id}', remove_sensor_data)

    app.router.add_get('/api/sensor-data', get_sensor_data)

# CRUD operations for SensorData
# curl -X GET http://localhost:8000/sensor_data/
async def list_sensor_data(request):
    """
    Retrieves a list of all sensor data.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing a list of sensor data.
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

# curl -X DELETE http://localhost:8000/sensor_data/
async def clear_sensor_data(request):
    """
    Deletes all sensor data.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: Response with status 204 (No Content).
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(SensorData))
            await session.commit()
            return web.Response(status=204)

#curl -X POST http://localhost:8000/sensor_data/ -H "Content-Type: application/json" -d '{"user_id": 1, "appId": "app123", "data": "temperature: 22", "messageType": "info", "ts": 1633036800}'
async def add_sensor_data(request):
    """
    Creates new sensor data.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the created sensor data.
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

# curl -X GET http://localhost:8000/sensor_data/1
async def show_sensor_data(request):
    """
    Retrieves specific sensor data by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the sensor data.
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

# curl -X PATCH http://localhost:8000/sensor_data/1 -H "Content-Type: application/json" -d '{"data": "temperature: 23"}'
async def update_sensor_data(request):
    """
    Updates specific sensor data by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the updated sensor data.
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

#curl -X DELETE http://localhost:8000/sensor_data/1
async def remove_sensor_data(request):
    """
    Deletes specific sensor data by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: Response with status 204 (No Content).
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
    Retrieves all sensor data.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing a list of all sensor data.
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
        
