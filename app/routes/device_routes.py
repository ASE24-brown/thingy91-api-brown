from app.handlers.device_handlers import get_all_sensor_data_for_device, get_device_status, get_all_device_statuses


def setup_device_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.
    
    Args:
        app (aiohttp.web.Application): The aiohttp application instance.
    Routes:
        - GET /devices/{device_id}/data: Retrieves all sensor data for a specific device.
        - GET /devices/{device_id}/status: Retrieves the status of a specific device.
        - GET /devices/status: Retrieves the status of all devices.
    """
    app.router.add_get('/devices/{device_id}/data', get_all_sensor_data_for_device)
    app.router.add_get('/devices/{device_id}/status', get_device_status)
    app.router.add_get('/devices/status', get_all_device_statuses)