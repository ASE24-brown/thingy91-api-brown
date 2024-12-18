import asyncio
import nest_asyncio
import os
import logging
from app import init_app
from aiohttp import web
from app.mqtt import start_mqtt_listener

log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level)

nest_asyncio.apply() 

async def main():
    """
    Main entry point for the application.

    Initializes the application, starts the MQTT listener, and runs the web application.

    Returns:
        None
    """
    app = await init_app()
    start_mqtt_listener(app)
    web.run_app(app, port=8000)

if __name__ == '__main__':
    asyncio.run(main())