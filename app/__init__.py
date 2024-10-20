from aiohttp import web
#from .routes import setup_routes
from .extensions import init_db, SessionLocal
#from .swagger import setup_swagger


async def init_app():
    """
    Initialize the application server
    
    """
    app = web.Application()
    await init_db()
    app['db'] = SessionLocal # initialize the database
    #setup_routes(app)
    #setup_swagger(app)

    return app
