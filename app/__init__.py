from aiohttp import web
from .extensions import setup_db
from .routes import setup_routes
from auth.auth import auth_middleware


async def init_app():
    """
    Initialize the application server
    
    """
    app = web.Application(middlewares=[auth_middleware])
    await setup_db(app)
    setup_routes(app)

    return app
