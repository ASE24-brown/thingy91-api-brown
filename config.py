import os

class Config:
    DATABASE_URL = 'sqlite+aiosqlite:///./thingy91.db'
    SECRET_KEY = os.environ.get('SECRET', 'mysecretkey')