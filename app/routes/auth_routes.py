from aiohttp import web
from auth import OAuth2Session
from config import CLIENT_ID, CLIENT_SECRET, AUTHORIZATION_BASE_URL, TOKEN_URL, REDIRECT_URI

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

def setup_auth_routes(app):
    app.add_routes(routes)