# oauth2_server.py

import logging
from flask import Flask, request, jsonify, redirect, url_for
from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6749.errors import OAuth2Error
from authlib.oauth2.rfc6749.models import ClientMixin
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['OAUTH2_REFRESH_TOKEN_GENERATOR'] = True

authorization = AuthorizationServer(app)

authorization_codes = {}

# In-memory store for clients and authorization codes
clients = {
    'your_client_id': {
        'client_id': 'your_client_id',
        'client_secret': 'your_client_secret',
        'redirect_uris': ['http://localhost:8000/callback'],
        'scope': 'openid profile email'
    }
}

class Client(ClientMixin):
    def __init__(self, client_id, client_secret, redirect_uris, scope, token_endpoint_auth_method="client_secret_basic", grant_types=None):
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
        # Verifies that the auth method used is the expected one
        return self.token_endpoint_auth_method == method
    
    def get_redirect_uri(self):
        return self.redirect_uris[0]

# Modify query_client to use both client_id and client_secret
def query_client(client_id, client_secret=None):
    # Sample client data, replace this with your actual data source
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
        logger.info(f"Querying authorization code: {code}")
        return authorization_codes.get(code)

    def delete_authorization_code(self, authorization_code):
        logger.info(f"Deleting authorization code: {authorization_code}")
        authorization_codes.pop(authorization_code.code, None)

    def authenticate_user(self, authorization_code):
        logger.info(f"Authenticating user with authorization code: {authorization_code}")
        return {'user_id': 'user'}

# Define the save_token function
def save_token(token, request):
    logger.info(f"Saving token: {token}")
    # Implement your token saving logic here
    # For example, you can save the token to a database or in-memory store
    # tokens[token['access_token']] = token

# Register the save_token function with the AuthorizationServer
authorization.save_token = save_token



authorization.query_client = query_client
authorization.register_grant(AuthorizationCodeGrant)
#authorization.register_client_auth_method('client_secret_basic', query_client)

@app.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
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

@app.route('/oauth/token', methods=['POST'])
def issue_token():
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
        return token
    except OAuth2Error as error:
        logger.error(f"OAuth2Error: {error}")
        return jsonify(error.get_body()), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000, ssl_context='adhoc')

