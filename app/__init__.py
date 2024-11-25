from aiohttp import web
from .extensions import setup_db
from .routes import setup_routes
import logging
import aiohttp
#from auth.auth import auth_middleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_callback(request):
    code = request.query.get('code')
    if not code:
        return web.Response(text="Authorization code not found", status=400)

    logger.info(f"Received authorization code: {code}")

    # Exchange the authorization code for an access token
    token_url = "http://auth_server:8001/oauth/token"
    client_id = "your_client_id"
    client_secret = "your_client_secret"
    redirect_uri = "http://localhost:8000/callback"

    async with aiohttp.ClientSession() as session:
        async with session.post(token_url, data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }) as resp:
            if resp.status != 200:
                logger.error(f"Failed to exchange authorization code: {resp.status}")
                return web.Response(text="Failed to exchange authorization code", status=resp.status)

            token_response = await resp.json()
            logger.info(f"Token response: {token_response}")

            # Handle the token response (e.g., store the access token)
            return web.Response(text=f"Access token: {token_response.get('access_token')}")


async def init_app():
    """
    Initialize the application server
    
    """
    #app = web.Application(middlewares=[auth_middleware])
    app = web.Application()
    app.router.add_get('/callback', handle_callback)
    await setup_db(app)
    setup_routes(app)

    return app
