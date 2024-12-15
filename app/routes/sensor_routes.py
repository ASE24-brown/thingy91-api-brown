from app.control.sensor_controller import list_sensor_data, clear_sensor_data, add_sensor_data, show_sensor_data, update_sensor_data, remove_sensor_data, get_sensor_data, get_all_sensor_data_for_user

def setup_sensor_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        - GET /sensor_data/: Retrieves a list of all sensor data.
        - DELETE /sensor_data/: Deletes all sensor data.
        - POST /sensor_data/: Adds new sensor data.
        - GET /sensor_data/{id}: Retrieves specific sensor data by ID.
        - PATCH /sensor_data/{id}: Updates specific sensor data by ID.
        - DELETE /sensor_data/{id}: Deletes specific sensor data by ID.
        - GET /api/sensor-data: Retrieves sensor data from the API.
    """
    
    app.router.add_get('/sensor_data/', list_sensor_data)
    app.router.add_delete('/sensor_data/', clear_sensor_data)
    app.router.add_post('/sensor_data/', add_sensor_data)
    
    app.router.add_get('/sensor_data/{id}', show_sensor_data)
    app.router.add_patch('/sensor_data/{id}', update_sensor_data)
    app.router.add_delete('/sensor_data/{id}', remove_sensor_data)
    app.router.add_get('/api/sensor-data', get_sensor_data)
    app.router.add_get('/sensor_data/user/{user_id}', get_all_sensor_data_for_user)