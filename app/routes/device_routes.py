from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData, Device
from app.handlers.device_handlers import get_all_sensor_data_for_device, get_device_status, get_all_device_statuses


def setup_device_routes(app):
    app.router.add_get('/devices/{device_id}/data', get_all_sensor_data_for_device)
    app.router.add_get('/devices/{device_id}/status', get_device_status)
    app.router.add_get('/devices/status', get_all_device_statuses)