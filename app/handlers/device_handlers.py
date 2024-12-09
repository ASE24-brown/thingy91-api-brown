from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData, Device
from app.extensions import SessionLocal


#Get All Sensor Data for a Device

async def get_all_sensor_data_for_device(db: Session, device_id: int):
    """
    Get all sensor data for a device.
    """
    async with SessionLocal() as session:
        async with session.begin():
            device_id = 1  # Replace with the desired device ID
            result = await session.execute(
                select(SensorData).where(SensorData.device_id == device_id)
            )
            sensor_data = result.scalars().all()
            for data in sensor_data:
                print(data.id, data.data, data.ts)


# Get All Sensor Data for a User's Devices

async def get_all_sensor_data_for_user_devices(db: Session, user_id: int):
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

async def get_sensor_data_with_user_and_device_info(db: Session, sensor_data_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                select(SensorData, Device, User)
                .join(Device, SensorData.device_id == Device.id)
                .join(User, Device.user_id == User.id)
            )
            for sensor_data, device, user in result:
                print(f"User: {user.username}, Device: {device.name}, Data: {sensor_data.data}")

