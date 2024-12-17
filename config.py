import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET', 'mysecretkey')
CLIENT_ID = os.environ.get('CLIENT_ID', 'your_client_id')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET', 'your_client_secret')
AUTHORIZATION_BASE_URL = 'http://localhost:8001/oauth/authorize'
TOKEN_URL = 'http://localhost:8001/oauth/token'
REDIRECT_URI = 'http://localhost:8000/callback'
DATABASE_URL = 'sqlite+aiosqlite:///./data/thingy91.db'