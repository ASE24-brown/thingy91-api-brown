from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from app.models import SensorData
from app.extensions import SessionLocal
from app.models import User, Device
from app.influxdb_client import write_api, query_api, INFLUXDB_BUCKET, INFLUXDB_ORG
from influxdb_client import Point
import asyncio
from datetime import datetime
import json
import os
import logging
from app.influxdb_client import INFLUXDB_ORG, INFLUXDB_BUCKET, query_api

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
        

async def get_sensor_data_for_user(request):
    """
    Get all sensor data from InfluxDB for a specific user based on the user_id.

    Args:
        request (web.Request): The request object containing the user ID in the path.

    Returns:
        web.Response: JSON response with the sensor data for the specified user.
    """
    user_id = request.match_info.get("user_id", "").strip()
    query = f"""
        from(bucket: "{INFLUXDB_BUCKET}")
            |> range(start: -30d)
            |> filter(fn: (r) => r["_measurement"] == "sensor_data")
            |> filter(fn: (r) => r["user_id"] == "{user_id}")
            |> filter(fn: (r) => r["_field"] == "data")
            |> filter(fn: (r) => r["_field"] == "value")  // Ensure only numeric fields are processed
            |> group(columns: ["appId"])
            |> mean()
        """
    print(f"Generated Flux query:\n{query}")

    
    try:
        # Query InfluxDB for the sensor data based on the user_id
        result = query_api.query(query, org=INFLUXDB_ORG)
        sensor_data = []
        
        # Format the result into a list of dictionaries
        for table in result:
            for record in table.records:
                sensor_data.append({
                    "id": record.get_value_by_key("device_id"),
                    "data": record.get_value_by_key("data"),
                    "timestamp": record.get_time().strftime('%Y-%m-%d %H:%M:%S'),
                    "appId": record.get_value_by_key("appId"),
                    "messageType": record.get_value_by_key("messageType"),
                })
        
        # Return the sensor data as a JSON response
        return web.json_response({"sensor_data": sensor_data})
    
    except Exception as e:
        return web.json_response({"error": f"Failed to query sensor data: {str(e)}"}, status=500)
    
from influxdb_client import InfluxDBClient
INFLUXDB_URL = os.environ.get("INFLUXDB_URL", "http://influxdb:8086")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")

client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
query_api = client.query_api()
write_api = client.write_api()

async def query_influx_data(request):
    try:
        # Correctly access the JSON data from the request body
        data = await request.json()  # Await the JSON body
        
        field_name = data.get('fieldName')  # Extract fieldName
        range = data.get('range', '-6h')  # Default to last 6 hours if range is not provided

        if not field_name:
            raise ValueError("Field name is required")

        # Construct the query for InfluxDB
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
        |> range(start: {range}, stop: now())
        |> filter(fn: (r) => r._measurement == "sensor_data")
        |> filter(fn: (r) => r.appId == "{field_name}")
        |> filter(fn: (r) => r._field == "data")
        |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
        |> yield(name: "mean")
        '''

        # Execute the query
        result = query_api.query(query)
        data = []
        for table in result:
            for record in table.records:
                data.append({
                    "_time": record.get_time().isoformat(),
                    "_value": record.get_value()
                })

        if not data:
            # Handle case when no data is found
            logging.warning(f"No data returned for field: {field_name}")
            return web.json_response({"error": "No data found"}, status=404)

        logging.debug(f"Query result from InfluxDB: {data}")
        
        # Return the data as a JSON response
        return web.json_response(data)

    except ValueError as ve:
        # Catch value errors (missing fieldName)
        logging.error(f"ValueError: {str(ve)}")
        return web.json_response({"error": str(ve)}, status=400)
    except Exception as e:
        # Catch other exceptions (e.g., InfluxDB errors)
        logging.error(f"Unexpected error: {str(e)}")
        return web.json_response({"error": str(e)}, status=500)