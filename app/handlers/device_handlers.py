from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models import User, SensorData, Device
from app.extensions import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.DEBUG)



async def check_device_status(session: AsyncSession):
    try:
        result = await session.execute(select(Device))
        devices = result.scalars().all()
        for device in devices:
            if datetime.now() - device.last_updated > timedelta(seconds=30):
                logging.debug(f"Device {device.id} is inactive. Updating status to 0.")
                device.status = 0
                session.add(device)
            else:
                logging.debug(f"Device {device.id} is active. Status remains 1.")
        logging.debug("Device statuses updated.")
    except Exception as e:
        logging.error(f"Error checking device statuses: {e}")


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


async def get_all_sensor_data_for_user_device(request):
    """
    Get all sensor data for a specific device belonging to a user.

    Args:
        request (web.Request): The request object containing the user ID and device ID.

    Returns:
        web.Response: A JSON response with the sensor data for the specified device and user.
    """
    user_id = request.match_info.get('user_id')  # Extract user_id from the request
    device_id = request.match_info.get('device_id')  # Extract device_id from the request

    if not user_id or not device_id:
        return web.json_response({"error": "User ID and Device ID are required"}, status=400)

    async with SessionLocal() as session:
        async with session.begin():
            # Verify the device is associated with the user
            device = await session.execute(
                select(Device).where(Device.id == device_id, Device.user_id == user_id)
            )
            device = device.scalar_one_or_none()
            
            if not device:
                return web.json_response({"error": "Device not found or does not belong to the user"}, status=404)

            # Fetch sensor data for the device
            result = await session.execute(
                select(SensorData).where(SensorData.device_id == device_id)
            )
            sensor_data = result.scalars().all()

            # Format the data
            data_list = [
                {"id": data.id, "data": data.data, "appID": data.appId, "ts": data.ts}
                for data in sensor_data
            ]

            return web.json_response(data_list)


async def get_all_device_statuses(request):
    """
    Get the status of all devices.

    Args:
        request (web.Request): The request object.

    Returns:
        web.Response: A JSON response with the statuses of all devices.
    """
    async with SessionLocal() as session:
        async with session.begin():
            logging.debug("Entering get_all_device_statuses function.")
            
            try:
                # Check and update device statuses within the same transaction
                await check_device_status(session)
                
                result = await session.execute(select(Device.id, Device.status, Device.last_updated))
                devices = result.all()
                logging.debug(f"Devices found: {devices}")
                
                if not devices:
                    logging.debug("No devices found in the database.")
                    return web.json_response({"error": "No devices found"}, status=404)

                # Create response data
                response_data = [
                    {
                        "device_id": device[0],  # Access tuple elements
                        "status": device[1],
                        "last_updated": device[2].isoformat()  # Ensure datetime serialization
                    }
                    for device in devices
                ]
                return web.json_response(response_data)
            except Exception as e:
                logging.error(f"Error fetching device statuses: {e}")
                return web.json_response({"error": "Internal server error"}, status=500)       

async def get_device_status(request):
    """
    Get the status of a device.

    Args:
        request (web.Request): The request object containing the device ID.

    Returns:
        web.Response: A JSON response with the status of the specified device.
    """
    device_id = request.match_info.get('device_id')  # Extract device_id from the request
    if not device_id:
        logging.error("Device ID is required but not provided.")
        return web.json_response({"error": "Device ID is required"}, status=400)

    logging.debug(f"Fetching status for device ID: {device_id}")

    async with SessionLocal() as session:
        async with session.begin():
            try:
                result = await session.execute(
                    select(Device).where(Device.id == device_id)
                )
                device = result.scalars().first()
                if not device:
                    logging.debug(f"Device with ID {device_id} not found.")
                    return web.json_response({"error": "Device not found"}, status=404)

                response_data = {
                    "device_id": device.id,
                    "status": device.status,
                    "last_updated": device.last_updated.isoformat()  # Ensure datetime serialization
                }
                logging.debug(f"Device status: {response_data}")
                return web.json_response(response_data)
            except Exception as e:
                logging.error(f"Error fetching device status: {e}")
                return web.json_response({"error": "Internal server error"}, status=500)

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

# Associate a Device with a User
async def associate_device_with_user2(request):
    """
    Associate a device with a user.

    Args:
        request (web.Request): The request object containing user_id and device_id.

    Returns:
        web.Response: A JSON response indicating success or failure.
    """
    data = await request.json()
    user_id = data.get("user_id")
    device_id = data.get("device_id")

    if not user_id or not device_id:
        return web.json_response({"error": "User ID and Device ID are required"}, status=400)

    async with SessionLocal() as session:
        async with session.begin():
            try:
                device = await session.get(Device, device_id)
                if not device:
                    return web.json_response({"error": "Device not found"}, status=404)

                device.user_id = user_id  # Associate the device with the user
                await session.commit()
                return web.json_response({"message": "Device successfully associated with user"})
            except IntegrityError as e:
                return web.json_response({"error": str(e)}, status=500)
            
async def associate_user_to_device(request):
    """
    Associate a user to a device.

    Args:
        request (web.Request): The request object containing the user ID and device ID.

    Returns:
        web.Response: A JSON response indicating success or failure.
    """
    data = await request.json()  # Parse the request body for user_id and device_id
    user_id = data.get("user_id")
    device_id = data.get("device_id")

    if not user_id or not device_id:
        return web.json_response({"error": "User ID and Device ID are required"}, status=400)

    async with SessionLocal() as session:
        async with session.begin():
            # Check if the user exists
            user = await session.execute(select(User).where(User.id == user_id))
            user = user.scalar_one_or_none()
            if not user:
                return web.json_response({"error": "User not found"}, status=404)

            # Check if the device exists
            device = await session.execute(select(Device).where(Device.id == device_id))
            device = device.scalar_one_or_none()
            if not device:
                return web.json_response({"error": "Device not found"}, status=404)

            # Associate the device with the user
            device.user_id = user_id
            session.add(device)  # Mark the device for update

            return web.json_response({"message": f"Device {device_id} is now associated with User {user_id}"})



