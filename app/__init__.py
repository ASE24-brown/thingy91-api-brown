import os
import json
from aiohttp import web
from .database import setup_db
from .routes import setup_routes
from aiohttp_swagger import setup_swagger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .control.device_controller import check_device_status
import pathlib


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

    # Serve static files for documentation
    docs_path = pathlib.Path(__file__).parent.parent / 'docs' / 'build' / 'html' 

    print(f"Serving static files from: {docs_path}")  # Debug print statement
    app.router.add_static('/docs/', path=docs_path, name='docs', show_index=True)
    
    setup_swagger(app, swagger_info=swagger_schema, swagger_url="/api/v1/doc", description="Thingy91 API", title="Thingy91 API")

    # Initialize the scheduler
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_device_status, 'interval', seconds=10, args=[app['db']])
    scheduler.start()
    return app
