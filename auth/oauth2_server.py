import logging
import uuid
import os
import jwt
import datetime
from flask import Flask, request, jsonify, redirect, url_for
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.errors import OAuth2Error
from authlib.oauth2.rfc6749.models import ClientMixin
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# Allow insecure transport for development
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

# Set the logging level based on an environment variable, default to INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True

authorization = AuthorizationServer(app)
authorization_codes = {}

def generate_access_token(user):
    payload = {
        "sub": user.id,
        "username": user.username,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)  # Token expire en 1 heure
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


class Client(ClientMixin):
    def __init__(self, client_id, client_secret, redirect_uris, scope, token_endpoint_auth_method="client_secret_basic", grant_types=None): 
        """
        Initialize the Client with the given parameters.

        Args:
            client_id (str): The client ID for the OAuth2 application.
            client_secret (str): The client secret for the OAuth2 application.
            redirect_uris (list): List of allowed redirect URIs.
            scope (str): The scope of the OAuth2 application.
            token_endpoint_auth_method (str): The authentication method for the token endpoint.
            grant_types (list): List of allowed grant types.
        """        
        self.id = client_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uris = redirect_uris
        self.scope = scope
        self.token_endpoint_auth_method = token_endpoint_auth_method  # Default authentication method
        self.grant_types = grant_types or ["authorization_code"]

    def get_client_id(self):
        """
        Get the client ID.

        Returns:
            str: The client ID.
        """
        return self.client_id

    def get_default_redirect_uri(self):
        """
        Get the default redirect URI.

        Returns:
            str: The default redirect URI.
        """
        return self.redirect_uris[0]

    def get_allowed_scope(self, scope):
        """
        Get the allowed scope.

        Args:
            scope (str): The requested scope.

        Returns:
            str: The allowed scope.
        """
        return scope

    def check_client_secret(self, client_secret):
        """
        Check if the provided client_secret matches the stored one.

        Args:
            client_secret (str): The client secret to check.

        Returns:
            bool: True if the client secret matches, False otherwise.
        """
        return self.client_secret == client_secret

    def check_redirect_uri(self, redirect_uri):
        """
        Check if the provided redirect_uri is allowed.

        Args:
            redirect_uri (str): The redirect URI to check.

        Returns:
            bool: True if the redirect URI is allowed, False otherwise.
        """
        return redirect_uri in self.redirect_uris

    def check_response_type(self, response_type):
        """
        Check if the provided response_type is allowed.

        Args:
            response_type (str): The response type to check.

        Returns:
            bool: True if the response type is allowed, False otherwise.
        """
        return response_type == 'code'

    def check_grant_type(self, grant_type):
        """
        Check if the provided grant_type is allowed.

        Args:
            grant_type (str): The grant type to check.

        Returns:
            bool: True if the grant type is allowed, False otherwise.
        """
        return grant_type in self.grant_types
    
    def check_endpoint_auth_method(self, method, endpoint):
        """
        Check if the provided endpoint authentication method is allowed.

        Args:
            method (str): The authentication method to check.
            endpoint (str): The endpoint to check.

        Returns:
            bool: True if the authentication method is allowed, False otherwise.
        """
        return self.token_endpoint_auth_method == method
    
    def get_redirect_uri(self):
        """
        Get the redirect URI.

        Returns:
            str: The redirect URI.
        """
        return self.redirect_uris[0]
    
clients = {
    'your_client_id': Client(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uris=['http://localhost:8000/callback'],
        scope='openid profile email'
    )
}

def query_client(client_id, client_secret=None):
    """
    Query the client based on client_id and optionally client_secret.

    Args:
        client_id (str): The client ID to query.
        client_secret (str, optional): The client secret to verify.

    Returns:
        Client: The Client object if found and verified, otherwise None.
    """
    logger.info(f"Querying client with client_id={client_id}")
    client = clients.get(client_id)
    if client_secret is None:
        return client
    if client and client.check_client_secret(client_secret):
        logger.info(f"Client credentials verified for client_id={client_id}")
        return client
    logger.warning(f"Invalid client credentials for client_id={client_id}")
    return None

class AuthorizationCode:
    """
    Represents an OAuth2 authorization code.

    Args:
        code (str): The authorization code.
        client_id (str): The client ID associated with the code.
        redirect_uri (str): The redirect URI associated with the code.
        scope (str): The scope associated with the code.
        state (str): The state associated with the code.
    """
    def __init__(self, code, client_id, redirect_uri, scope, state):
        """
        Initialize the AuthorizationCode with the given parameters.
        """
        self.code = code
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    def get_redirect_uri(self):
        """
        Get the redirect URI.

        Returns:
            str: The redirect URI.
        """
        return self.redirect_uri
    
    def get_scope(self):
        """
        Get the scope.

        Returns:
            str: The scope.
        """
        return self.scope


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        """
        Save the authorization code.

        Args:
            code (dict): The authorization code to save.
            request (Request): The request object.
        """
        logger.info(f"Saving authorization code: {code}")
        authorization_code = AuthorizationCode(
            code=code['code'],
            client_id=code['client_id'],
            redirect_uri=code['redirect_uri'],
            scope=code['scope'],
            state=code['state']
        )
        authorization_codes[code['code']] = code

    def query_authorization_code(self, code, client):
        """
        Query the authorization code.

        Args:
            code (str): The authorization code to query.
            client (Client): The client associated with the code.

        Returns:
            AuthorizationCode: The authorization code if found, otherwise None.
        """
        logger.info(f"Querying authorization code: {code}")
        return authorization_codes.get(code)

    def delete_authorization_code(self, authorization_code):
        """
        Delete the authorization code.

        Args:
            authorization_code (AuthorizationCode): The authorization code to delete.
        """
        logger.info(f"Deleting authorization code: {authorization_code}")
        authorization_codes.pop(authorization_code.code, None)

    def authenticate_user(self, authorization_code):
        """
        Authenticate the user with the authorization code.

        Args:
            authorization_code (AuthorizationCode): The authorization code to authenticate.

        Returns:
            dict: The user information.
        """
        logger.info(f"Authenticating user with authorization code: {authorization_code}")
        return {'user_id': 'user'}


def save_token(token, request):
    """
    Save the token.

    Args:
        token (dict): The token to save.
        request (Request): The request object.
    """
    logger.info(f"Saving token: {token}")
    #tokens[token['access_token']] = token

@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """
    Handle the authorization request without showing a form.

    Args:
        request (Request): The request object.

    Returns:
        Response: A redirect response to the client with the authorization code.
    """
    client_id = request.args.get('client_id')
    redirect_uri = request.args.get('redirect_uri')
    scope = request.args.get('scope')
    state = request.args.get('state')
    response_type = request.args.get('response_type')

    # Automatically generate an authorization code
    code = str(uuid.uuid4())
    authorization_codes[code] = AuthorizationCode(
        code=code,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
    )

    # Redirect to the client with the authorization code
    return redirect(f"{redirect_uri}?code={code}&state={state}")


@app.route('/oauth/token', methods=['POST'])
def token():
    """
    Exchange authorization code for an access token.

    Args:
        request (Request): The request object.

    Returns:
        Response: A JSON response with the access token or an error message.
    """
    code = request.form.get('code')
    client_id = request.form.get('client_id')
    redirect_uri = request.form.get('redirect_uri')

    logger.info(f"Token request received: code={code}, client_id={client_id}, redirect_uri={redirect_uri}")

    # Validate the authorization code
    if code not in authorization_codes:
        logger.error("Invalid or expired authorization code.")
        return jsonify({"error": "invalid_grant"}), 400

    auth_code_data = authorization_codes.pop(code)  # Remove the code after use

    # Validate client_id and redirect_uri
    if auth_code_data.client_id != client_id or auth_code_data.redirect_uri != redirect_uri:
        logger.error("Invalid client_id or redirect_uri.")
        return jsonify({"error": "invalid_client"}), 400

    # Generate an access token (and optionally a refresh token)
    access_token = str(uuid.uuid4())
    logger.info(f"Access token generated: {access_token}")

    # Send the token response
    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600,  # Token expiry in seconds
        "scope": auth_code_data.scope,
    })


authorization.save_token = save_token
authorization.query_client = query_client
authorization.register_grant(AuthorizationCodeGrant)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

