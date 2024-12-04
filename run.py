from app import init_app
from aiohttp import web
import asyncio
import nest_asyncio
from mqtt import start_mqtt_listener
from config import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL, REDIRECT_URI
from auth import OAuth2Session
import os
import logging

# Set the logging level based on an environment variable, default to INFO
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level)


nest_asyncio.apply() 

async def main():
    app = await init_app()
    start_mqtt_listener(app)
    web.run_app(app, port=8000)

if __name__ == '__main__':
    asyncio.run(main())