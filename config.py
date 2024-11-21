import os

class Config:
    DATABASE_URL = 'sqlite+aiosqlite:///./thingy91.db'
    SECRET_KEY = os.environ.get('SECRET', 'mysecretkey')


# config.py
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
AUTHORIZATION_BASE_URL = 'http://localhost:8001/oauth/authorize'
TOKEN_URL = 'http://localhost:8001/oauth/token'
REDIRECT_URI = 'http://localhost:8000/callback'