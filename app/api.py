from aiohttp import web
from app.data_handlers import (list_users, clear_users, add_user, show_user, update_user, remove_user)
from app.data_handlers import (list_profiles, clear_profiles, add_profile, show_profile, update_profile, remove_profile )
from app.data_handlers import (list_sensor_data, clear_sensor_data, add_sensor_data, show_sensor_data, update_sensor_data, remove_sensor_data)
from app.data_handlers import get_sensor_data

    #get_profiles_for_user, add_profile_to_user, get_users_by_profile, get_sensor_data_for_user

from app.extensions import reset_db

async def reset_database(request):
    """
    Resets the database by deleting all records from all tables.
    """
    await reset_db()
    return web.json_response({"status": "database reset"})

def setup_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /users/: Retrieves a list of all users.
        DELETE /users/: Deletes all users.
        POST /users/: Creates a new user with a profile.
        GET /users/{id}: Retrieves a specific user by ID.
        PATCH /users/{id}: Updates a specific user by ID.
        DELETE /users/{id}: Deletes a specific user by ID.
        GET /users/{id}/sensor_data: Retrieves all sensor data for a specific user.
        
        GET /profiles/: Retrieves a list of all profiles.
        DELETE /profiles/: Deletes all profiles.
        POST /profiles/: Creates a new profile.
        GET /profiles/{id}: Retrieves a specific profile by ID.
        PATCH /profiles/{id}: Updates a specific profile by ID.
        DELETE /profiles/{id}: Deletes a specific profile by ID.
        
        GET /users/{id}/profiles: Retrieves the profile for a specific user.
        POST /users/{id}/profiles: Adds a profile to a specific user.
        GET /profiles/{id}/users: Retrieves the user associated with a specific profile.
        
        GET /sensor_data/: Retrieves a list of all sensor data.
        DELETE /sensor_data/: Deletes all sensor data.
        POST /sensor_data/: Adds new sensor data.
        GET /sensor_data/{id}: Retrieves specific sensor data by ID.
        PATCH /sensor_data/{id}: Updates specific sensor data by ID.
        DELETE /sensor_data/{id}: Deletes specific sensor data by ID.
        
        POST /reset_db: Resets the database.
    """
    app.router.add_get('/users/', list_users)
    app.router.add_delete('/users/', clear_users)
    app.router.add_post('/users/', add_user)
    app.router.add_get('/users/{id}', show_user)
    app.router.add_patch('/users/{id}', update_user)
    app.router.add_delete('/users/{id}', remove_user)
    
    #app.router.add_get('/users/{id}/sensor_data', get_sensor_data_for_user) 
    
    app.router.add_get('/profiles/', list_profiles)
    app.router.add_delete('/profiles/', clear_profiles)
    app.router.add_post('/profiles/', add_profile)
    app.router.add_get('/profiles/{id}', show_profile)
    app.router.add_patch('/profiles/{id}', update_profile)
    app.router.add_delete('/profiles/{id}', remove_profile)
    
    #app.router.add_get('/users/{id}/profiles', get_profiles_for_user)
    #app.router.add_post('/users/{id}/profiles', add_profile_to_user)
    #app.router.add_get('/profiles/{id}/users', get_users_by_profile)
    
    app.router.add_get('/sensor_data/', list_sensor_data)
    app.router.add_delete('/sensor_data/', clear_sensor_data)
    app.router.add_post('/sensor_data/', add_sensor_data)
    app.router.add_get('/sensor_data/{id}', show_sensor_data)
    app.router.add_patch('/sensor_data/{id}', update_sensor_data)
    app.router.add_delete('/sensor_data/{id}', remove_sensor_data)


    app.router.add_get('/api/sensor-data', get_sensor_data)
    
    app.router.add_post('/reset_db', reset_database)  # Temporary route to reset the database

    # Print detailed information about the routes
    for route in app.router.routes():
        print(f"Route: {route.method} {route.resource}")