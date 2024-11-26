import os
import jwt
import datetime
from aiohttp import web
import bcrypt
import requests
import uuid
from sqlalchemy.future import select
from app.models import User
from app.extensions import SessionLocal
from datetime import datetime, timedelta
from authlib.oauth2.rfc6749 import OAuth2Request
from .oauth2_server import authorization, authorization_codes, AuthorizationCode



SECRET_KEY = "your_secret_key"  # À remplacer par une clé sécurisée

async def login_user(request):
    """
    Handle user login.

    :param request: The request object.
    :return: The login response.
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

                # Exchange authorization code for access token
                #token_url = 'http://localhost:8000/oauth/token'
                #token_data = {
                #    'client_id': 'your_client_id',
                #    'client_secret': 'your_client_secret',
                #    'grant_type': 'authorization_code',
                #    'code': code,
                #    'redirect_uri': 'http://localhost:8000/callback'
                #}
                #token_response = requests.post(token_url, data=token_data)
                #token_response.raise_for_status()
                #token_data = token_response.json()

                # Generate JWT token
                jwt_token = jwt.encode(
                    {
                        "user_id": user.id,
                        "exp": datetime.now() + timedelta(hours=1)
                    },
                    SECRET_KEY,  # Replace with your actual secret key
                    algorithm="HS256"
                )

                return web.json_response({"message": "Login successful", "token": jwt_token}, status=200)
            else:
                return web.json_response({"error": "Invalid username or password"}, status=401)