from app import init_app
from aiohttp import web
import asyncio
import nest_asyncio
from app.mqtt_handler import start_mqtt_listener, retrieve_data

nest_asyncio.apply()

async def main():
    app = await init_app()
    start_mqtt_listener(app)
    web.run_app(app, host='127.0.0.1', port=8080)

if __name__ == '__main__':
    asyncio.run(main())