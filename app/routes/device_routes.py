from app.control.device_controller import get_all_sensor_data_for_device, get_device_status, get_all_device_statuses, get_all_sensor_data_for_user_device
from app.control.device_controller import associate_user_to_device, disassociate_device_from_user

def setup_device_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.
    
    Args:
        app (aiohttp.web.Application): The aiohttp application instance.
        
    Routes:
        - GET /devices/{device_id}/data: Retrieves all sensor data for a specific device.
        - GET /devices/{device_id}/status: Retrieves the status of a specific device.
        - GET /devices/status: Retrieves the status of all devices.
        - POST /associate-user-to-device: Associates a user to a device.
        - POST /disassociate-device-from-user: Disassociates a device from a user.
        - GET /users/{user_id}/devices/{device_id}/data: Retrieves all sensor data for a specific device belonging to a user.
    """
    app.router.add_get('/devices/{device_id}/status', get_device_status)
    app.router.add_get('/devices/status', get_all_device_statuses)

    app.router.add_post('/associate-user-to-device', associate_user_to_device)
    app.router.add_post('/disassociate-device-from-user', disassociate_device_from_user)

    app.router.add_get('/devices/{device_id}/data', get_all_sensor_data_for_device)
    app.router.add_get('/users/{user_id}/devices/{device_id}/data', get_all_sensor_data_for_user_device)