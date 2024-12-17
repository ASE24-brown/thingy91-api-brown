from aiohttp import web
from .user_routes import setup_user_routes
from .sensor_routes import setup_sensor_routes
from .device_routes import setup_device_routes
from .auth_routes import setup_auth_routes


def setup_routes(app):
    """
    Configure all the routes for the application.

    Args:
        app (aiohttp.web.Application): Instance of the aiohttp application.
    """
    setup_user_routes(app)
    setup_auth_routes(app)
    setup_sensor_routes(app)
    setup_device_routes(app)

    # Print detailed information about the routes
    for route in app.router.routes():
        print(f"Route: {route.method} {route.resource}")