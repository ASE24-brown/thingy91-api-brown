import json
import os
import jwt
import datetime
from aiohttp import web
import aiohttp
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SECRET_KEY = "your_secret_key"

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