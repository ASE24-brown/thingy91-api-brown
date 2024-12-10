from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData, Device
from app.extensions import SessionLocal


#Get All Sensor Data for a Device

async def get_all_sensor_data_for_device(request):
    """
    Get all sensor data for a device.

    Args:
        request (web.Request): The request object containing the device ID.

    Returns:
        web.Response: A JSON response with the sensor data for the specified device.
    """
    device_id = request.match_info.get('device_id')  # Extract device_id from the request
    if not device_id:
        return web.json_response({"error": "Device ID is required"}, status=400)

    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(SensorData).where(SensorData.device_id == device_id)
            )
            sensor_data = result.scalars().all()
            data_list = [{"id": data.id, "data": data.data, "appID": data.appId, "ts": data.ts} for data in sensor_data]
            return web.json_response(data_list)


# Get All Sensor Data for a User's Devices
async def get_all_sensor_data_for_user_devices(request):
    async with SessionLocal() as session:
        async with session.begin():
            user_id = 1  # Replace with the desired user ID
            result = await session.execute(
                select(SensorData).join(Device).where(Device.user_id == user_id)
            )
            sensor_data = result.scalars().all()
            for data in sensor_data:
                print(data.id, data.data, data.ts)

#  Get Sensor Data with User and Device Info
async def get_sensor_data_with_user_and_device_info(request):
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(SensorData, Device, User)
                .join(Device, SensorData.device_id == Device.id)
                .join(User, Device.user_id == User.id)
            )
            for sensor_data, device, user in result:
                print(f"User: {user.username}, Device: {device.name}, Data: {sensor_data.data}")

