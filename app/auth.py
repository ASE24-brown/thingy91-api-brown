# auth.py
import aiohttp
from oauthlib.oauth2 import WebApplicationClient
from oauthlib.oauth2.rfc6749.errors import InsecureTransportError
import json

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class OAuth2Session(aiohttp.ClientSession):
    def __init__(self, client_id, client_secret, authorization_base_url, token_url, redirect_uri, **kwargs):
        super().__init__(**kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_base_url = authorization_base_url
        self.token_url = token_url
        self.redirect_uri = redirect_uri
        self.client = WebApplicationClient(client_id)

    async def fetch_token(self, code):
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
                return token
        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status} - {e.message}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def authorization_url(self):
        # Disable HTTPS check for development
        self.client._insecure_transport = True
        return self.client.prepare_request_uri(self.authorization_base_url, redirect_uri=self.redirect_uri)