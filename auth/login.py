import os
import jwt
import datetime
from aiohttp import web
import logging
import aiohttp
import bcrypt
import requests
import uuid
from sqlalchemy.future import select
from app.model.device import Device
from app.model.sensor_data import SensorData
from app.model.user import User
from app.database import SessionLocal
from datetime import datetime, timedelta
from authlib.oauth2.rfc6749 import OAuth2Request
from .oauth2_server import authorization, authorization_codes, AuthorizationCode
from config import SECRET_KEY


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_callback(request):
    """
    Handles the OAuth2 callback by exchanging the authorization code for an access token.

    Args:
        request: The request object containing the authorization code.

    Returns:
        web.Response: A response with the access token or an error message.
    """
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

async def login_user(request):
    """
    Authenticates a user and returns a JWT token if successful.

    Args:
        request: The request object containing the username and password.

    Returns:
        web.json_response: A JSON response with the JWT token or an error message.
    """
    data = await request.json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return web.json_response({"error": "Missing required fields"}, status=400)

    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.username == username))
            user = result.scalars().first()

            if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
                # Generate authorization code
                code = str(uuid.uuid4())
                authorization_code = AuthorizationCode(
                    code=code,
                    client_id='your_client_id',
                    redirect_uri='http://localhost:8000/callback',
                    scope='openid profile email',
                    state=''
                )
                authorization_codes[code] = authorization_code
                # Generate JWT token
                jwt_token = jwt.encode(
                    {
                        "user_id": user.id,
                        "exp": datetime.now() + timedelta(hours=1)
                    },
                    SECRET_KEY, 
                    algorithm="HS256"
                )

                return web.json_response({"message": "Login successful", "token": jwt_token}, status=200)
            else:
                return web.json_response({"error": "Invalid username or password"}, status=401)