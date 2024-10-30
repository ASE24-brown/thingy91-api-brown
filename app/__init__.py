from aiohttp import web
#from .routes import setup_routes
from .extensions import init_db, SessionLocal
#from .swagger import setup_swagger
from .data_routes import get_sensor_data

async def init_app():
    """
    Initialize the application server
    
    """
    app = web.Application()
    await init_db()
    app['db'] = SessionLocal # initialize the database
    app.router.add_get('/api/sensor-data', get_sensor_data)
    #setup_routes(app)
    #setup_swagger(app)

    return app
