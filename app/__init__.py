import os
import json
from aiohttp import web
from .extensions import setup_db
from .routes import setup_routes
from aiohttp_swagger import setup_swagger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .handlers.device_handlers import check_device_status
from datetime import datetime, timedelta
from sqlalchemy.future import select
from .models import Device

# Load swagger file
swagger_path = os.path.join(os.path.dirname(__file__), '..', 'swagger', 'swagger.json')
with open(swagger_path, "r") as file:
    swagger_schema = json.load(file)

swagger_dir = os.path.join(os.path.dirname(__file__), '..', 'swagger', 'paths')


async def init_app():
    """
    Initialize the application server

    Returns: 
        app (aiohttp.web.Application): The aiohttp application instance.
    """
    app = web.Application()
    await setup_db(app)
    setup_routes(app)
    # Serve static files from the swagger directory
    #app.router.add_static('/api/v1/doc/paths', os.path.join(os.path.dirname(__file__), '..', 'swagger', 'paths'))
        # Serve static files from the swagger directory
    #print(f"Serving static files from: {swagger_dir}")
    #app.router.add_static('/api/v1/doc/paths', swagger_dir)
    
    setup_swagger(app, swagger_info=swagger_schema, swagger_url="/api/v1/doc", description="Thingy91 API", title="Thingy91 API")

    # Initialize the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_device_status, 'interval', seconds=30, args=[app['db']])
    scheduler.start()
    return app
