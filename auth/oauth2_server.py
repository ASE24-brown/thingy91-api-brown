# oauth2_server.py

import logging
from flask import Flask, request, jsonify, redirect, url_for
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.errors import OAuth2Error
from authlib.oauth2.rfc6749.models import ClientMixin
import uuid
import os
import jwt
import datetime
SECRET_KEY = "your_secret_key"  # À remplacer par une clé sécurisée



# Set the logging level based on an environment variable, default to INFO
log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level)

# Allow insecure transport for development
os.environ['AUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True

authorization = AuthorizationServer(app)

authorization_codes = {}

# In-memory store for clients and authorization codes

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

        :param client_id: The client ID for the OAuth2 application.
        :param client_secret: The client secret for the OAuth2 application.
        :param redirect_uris: List of allowed redirect URIs.
        :param scope: The scope of the OAuth2 application.
        :param token_endpoint_auth_method: The authentication method for the token endpoint.
        :param grant_types: List of allowed grant types.
        """        
        self.id = client_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uris = redirect_uris
        self.scope = scope
        self.token_endpoint_auth_method = token_endpoint_auth_method  # Default authentication method
        self.grant_types = grant_types or ["authorization_code"]

    def get_client_id(self):
        return self.client_id

    def get_default_redirect_uri(self):
        return self.redirect_uris[0]

    def get_allowed_scope(self, scope):
        return scope

    def check_client_secret(self, client_secret):
        # Checks if the provided client_secret matches the stored one
        return self.client_secret == client_secret

    def check_redirect_uri(self, redirect_uri):
        return redirect_uri in self.redirect_uris

    def check_response_type(self, response_type):
        return response_type == 'code'

    def check_grant_type(self, grant_type):
        return grant_type in self.grant_types
    def check_endpoint_auth_method(self, method, endpoint):
        return self.token_endpoint_auth_method == method
    
    def get_redirect_uri(self):
        return self.redirect_uris[0]
    
clients = {
    'your_client_id': Client(
        client_id='your_client_id',
        client_secret='your_client_secret',
        redirect_uris=['http://localhost:8000/callback'],
        scope='openid profile email'
    )
}



def query_client(client_id, client_secret=None):
    logger.info(f"Querying client with client_id={client_id}")
    client = clients.get(client_id)
    if client_secret is None:
        return client
    if client and client.check_client_secret(client_secret):
        logger.info(f"Client credentials verified for client_id={client_id}")
        return client
    logger.warning(f"Invalid client credentials for client_id={client_id}")
    return None

def query_client2(client_id, client_secret=None):
    """
    Query the client based on client_id and optionally client_secret.

    :param client_id: The client ID to query.
    :param client_secret: The client secret to verify.
    :return: The Client object if found and verified, otherwise None.
    """
    client_data = {
        'client_id': 'your_client_id',
        'client_secret': 'your_client_secret',
        'redirect_uris': ['http://localhost:8000/callback'],
        'scope': 'openid profile email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'grant_types': ['authorization_code']  # Ensure grant_types is included
    }

    # Check if client_id matches
    if client_data['client_id'] == client_id:
        # Instantiate a Client object with the provided data
        client = Client(
            client_id=client_data['client_id'],
            client_secret=client_data['client_secret'],
            redirect_uris=client_data['redirect_uris'],
            scope=client_data['scope'],
            token_endpoint_auth_method=client_data['token_endpoint_auth_method'],
            grant_types=client_data.get('grant_types')  # Use get to provide a default value
        )
        # If client_secret is provided, check if it matches
        if client_secret is None or client.check_client_secret(client_secret):
            return client
    return None

class AuthorizationCode:
    """
    Initialize the AuthorizationCode with the given parameters.

    :param code: The authorization code.
    :param client_id: The client ID associated with the code.
    :param redirect_uri: The redirect URI associated with the code.
    :param scope: The scope associated with the code.
    :param state: The state associated with the code.
    """
    def __init__(self, code, client_id, redirect_uri, scope, state):
        self.code = code
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state

    def get_redirect_uri(self):
        return self.redirect_uri
    
    def get_scope(self):
        return self.scope


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    def save_authorization_code(self, code, request):
        """
        Save the authorization code.

        :param code: The authorization code to save.
        :param request: The request object.
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

        :param code: The authorization code to query.
        :param client: The client associated with the code.
        :return: The authorization code if found, otherwise None.
        """
        logger.info(f"Querying authorization code: {code}")
        return authorization_codes.get(code)

    def delete_authorization_code(self, authorization_code):
        """
        Delete the authorization code.

        :param authorization_code: The authorization code to delete.
        """
        logger.info(f"Deleting authorization code: {authorization_code}")
        authorization_codes.pop(authorization_code.code, None)

    def authenticate_user(self, authorization_code):
        """
        Authenticate the user with the authorization code.

        :param authorization_code: The authorization code to authenticate.
        :return: The user information.
        """
        logger.info(f"Authenticating user with authorization code: {authorization_code}")
        return {'user_id': 'user'}

# Define the save_token function
def save_token(token, request):
    """
    Save the token.

    :param token: The token to save.
    :param request: The request object.
    """
    logger.info(f"Saving token: {token}")
    # Implement token saving logic here
    # Save the token to a database or in-memory store
    # tokens[token['access_token']] = token

authorization.save_token = save_token
authorization.query_client = query_client
authorization.register_grant(AuthorizationCodeGrant)

@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """
    Handle the authorization request.

    :return: The authorization response.
    """
    if request.method == 'GET':
        # Display the authorization page
        client_id = request.args.get('client_id')
        redirect_uri = request.args.get('redirect_uri')
        response_type = request.args.get('response_type')
        scope = request.args.get('scope')
        state = request.args.get('state')
        logger.info(f"Authorization request: client_id={client_id}, redirect_uri={redirect_uri}, response_type={response_type}, scope={scope}, state={state}")
        return f'''
        <form method="post">
            <p>Client ID: <input type="text" id="client_id" name="client_id" value="{client_id or ''}"></p>
            <p>Redirect URI: <input type="text" id="redirect_uri" name="redirect_uri" value="{redirect_uri or ''}"></p>
            <p>Response Type: <input type="text" id="response_type" name="response_type" value="{response_type or ''}"></p>
            <p>Scope: <input type="text" id="scope" name="scope" value="{scope or ''}"></p>
            <p>State: <input type="text" id="state" name="state" value="{state or ''}"></p>
            <button type="submit">Authorize</button>
        </form>
        '''
    if request.method == 'POST':
        # Handle the authorization request
        code = str(uuid.uuid4())  # Generate a real authorization code
        client_id = request.form.get('client_id')
        redirect_uri = request.form.get('redirect_uri')
        scope = request.form.get('scope')
        state = request.form.get('state')
        authorization_code = {
            'code': code,
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'scope': scope,
            'state': state
        }
        logger.info(f"Generated authorization code: {authorization_code}")
        authorization_codes[code] = AuthorizationCode(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            state=state
        )
        return redirect(f'{redirect_uri}?code={code}')

#@app.route('/oauth/token', methods=['POST'])
def issue_token2():
    """
    Issue the token.

    :return: The token response.
    """
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    # Check client credentials
    client = query_client(client_id, client_secret)
    if not client:
        logger.warning("Invalid client credentials")
        return jsonify({"error": "invalid_client"}), 401

    try:
        logger.info("Issuing token")
        token = authorization.create_token_response()
        logger.info(f"Token response: {token}")
        return token
    except OAuth2Error as error:
        logger.error(f"OAuth2Error: {error}")
        return jsonify(error.get_body()), error.status_code

@app.route('/oauth/token', methods=['POST'])
def issue_token():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')
    logger.info(f"Received token request: client_id={client_id}, client_secret={client_secret}")

    client = query_client(client_id, client_secret)
    if not client:
        logger.warning(f"Invalid client credentials: client_id={client_id}, client_secret={client_secret}")
        return jsonify({"error": "invalid_client"}), 401

    try:
        logger.info("Generating token response")
        token = generate_access_token(client)
        token_response = {
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': 3600  # Token validity in seconds
        }
        logger.info(f"Generated token response: {token_response}")
        return jsonify(token_response), 200
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "server_error"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

