from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData, Device
from app.handlers.device_handlers import get_all_sensor_data_for_device


def setup_device_routes(app):
    app.router.add_get('/devices/{device_id}/data', get_all_sensor_data_for_device)