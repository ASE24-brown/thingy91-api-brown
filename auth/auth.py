import aiohttp
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError
import json
import os
import jwt
import datetime
from aiohttp import web
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#from services.user_service import authenticate_user

#SECRET_KEY = "your_secret_key"  # À remplacer par une clé sécurisée

class OAuth2Session(aiohttp.ClientSession):
    def __init__(self, client_id, client_secret, authorization_base_url, token_url, redirect_uri, **kwargs):
        """
        Initialize the OAuth2Session with the given parameters.

        :param client_id: The client ID for the OAuth2 application.
        :param client_secret: The client secret for the OAuth2 application.
        :param authorization_base_url: The base URL for the authorization endpoint.
        :param token_url: The URL for the token endpoint.
        :param redirect_uri: The redirect URI for the OAuth2 application.
        :param kwargs: Additional keyword arguments to pass to the aiohttp.ClientSession.
        """
        super().__init__(**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.client = WebApplicationClient(client_id)
    
    def generate_jwt_token(self):
        """
        Generate a JWT token for the OAuth2 application.
        
        :param client_id: The client ID for the OAuth2 application.
        :return: The JWT token as a string.
        """
        payload = {
            'client_id': self.client_id,
            'exp': datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expiration time
        }
        token = jwt.encode(payload, self.client_secret, algorithm='HS256')
        return token
    

    async def fetch_token(self, code):
        """
        Fetch the OAuth2 token using the provided authorization code.

        :param code: The authorization code received from the authorization server.
        :return: The token response as a dictionary.
        """
        try:
            token_url, headers, body = self.client.prepare_token_request(
                self.token_url,
                authorization_response=f"{self.redirect_uri}?code={code}",
                redirect_url=self.redirect_uri,
                code=code
            )
            async with self.post(token_url, headers=headers, data=body, auth=aiohttp.BasicAuth(self.client_id, self.client_secret)) as response:
                response.raise_for_status()  # Raise an exception for HTTP errors
                token = await response.json()
                self.client.parse_request_body_response(json.dumps(token))
                # Generate JWT token and add it to the response
                jwt_token = self.generate_jwt_token()
                token['jwt_token'] = jwt_token
                
                return token
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def authorization_url(self):
        """
        Generate the authorization URL for the OAuth2 application.

        :return: The authorization URL as a string.
        """
        # Disable HTTPS check for development
        self.client._insecure_transport = True
        return self.client.prepare_request_uri(self.authorization_base_url, redirect_uri=self.redirect_uri)
"""    
def generate_access_token(user):
    payload = {
        "sub": user.id,
        "username": user.username,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expire en 1 heure
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

async def auth_middleware(app, handler):
    async def middleware_handler(request):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return web.json_response({"error": "Unauthorized"}, status=401)

        token = token.split("Bearer ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request["user"] = {"id": payload["sub"], "username": payload["username"]}
        except jwt.ExpiredSignatureError:
            return web.json_response({"error": "Token expired"}, status=401)
        except jwt.InvalidTokenError:
            return web.json_response({"error": "Invalid token"}, status=401)

        return await handler(request)

    return middleware_handler

async def token_endpoint(request):
    #"""
    #OAuth2 Token endpoint.
    #Expects a POST request with grant_type, username, password, etc.
    #"""
"""
    data = await request.post()
    grant_type = data.get("grant_type")

    if grant_type != "password":
        return web.json_response({"error": "unsupported_grant_type"}, status=400)

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return web.json_response({"error": "invalid_request", "error_description": "Username and password are required."}, status=400)

    async with request.app["db_session"]() as session:
        user = await authenticate_user(session, username, password)
        if not user:
            return web.json_response({"error": "invalid_grant", "error_description": "Invalid credentials."}, status=400)

        # Générer un access token (JWT)
        token = generate_access_token(user)

        return web.json_response({
            "access_token": token,
            "token_type": "Bearer",
            "expires_in": 3600,  # Durée en secondes
        }, status=200)

"""