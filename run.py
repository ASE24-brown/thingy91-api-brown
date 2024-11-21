from app import init_app
from aiohttp import web
import asyncio
import nest_asyncio
from app.mqtt_handler import start_mqtt_listener, retrieve_data
from config import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL, REDIRECT_URI
from app.auth import OAuth2Session

nest_asyncio.apply()

routes = web.RouteTableDef()

@routes.get('/login')
async def login(request):
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL, REDIRECT_URI)
    authorization_url = oauth.authorization_url()
    return web.HTTPFound(authorization_url)

@routes.get('/callback')
async def callback(request):
    code = request.query.get('code')
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL, REDIRECT_URI)
    token = await oauth.fetch_token(code)
    return web.json_response(token)

async def main():
    app = await init_app()
    start_mqtt_listener(app)
    app.add_routes(routes)  # Add OAuth2 routes to the app
    web.run_app(app, port=8000)

if __name__ == '__main__':
    asyncio.run(main())