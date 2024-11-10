from aiohttp import web
from .api import setup_routes
from .extensions import setup_db

#from .swagger import setup_swagger

async def init_app():
    """
    Initialize the application server
    
    """
    app = web.Application()
    await setup_db(app)
    setup_routes(app)
    
    #setup_swagger(app)

    return app
