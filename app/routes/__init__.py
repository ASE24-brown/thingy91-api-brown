from aiohttp import web
from .user_routes import setup_user_routes
from .sensor_routes import setup_sensor_routes
from .profile_routes import setup_profile_routes
from .auth_routes import setup_auth_routes
from app.extensions import reset_db

async def reset_database(request):
    """
    Resets the database by deleting all records from all tables.
    """
    await reset_db()
    return web.json_response({"status": "database reset"})

def setup_routes(app):
    """
    Configure all the routes for the application.

    :param app: Instance of the aiohttp application
    """
    # Add routes for users
    setup_user_routes(app)
    # Add routes for sensors
    setup_sensor_routes(app)
    # Add routes for profiles
    setup_profile_routes(app)
    # Add routes for authentication
    setup_auth_routes(app)

    # Temporary route to reset the database
    app.router.add_post('/reset_db', reset_database)  

    # Print detailed information about the routes
    for route in app.router.routes():
        print(f"Route: {route.method} {route.resource}")