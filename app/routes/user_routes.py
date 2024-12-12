from aiohttp import web
import aiohttp
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
import jwt
import bcrypt
from datetime import datetime, timedelta
from app.models import User
from app.extensions import SessionLocal
import logging
from auth.login import login_user, handle_callback
from app.handlers.user_handlers import list_users, clear_users, add_user, show_user, update_user, remove_user, register_user, login_user

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_user_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application with OpenAPI-compatible documentation for aiohttp-swagger.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        - GET /users/: Retrieves a list of all users.
        - DELETE /users/: Deletes all users.
        - POST /users/: Creates a new user with a profile.
        - GET /users/{id}: Retrieves a specific user by ID.
        - PATCH /users/{id}: Updates a specific user by ID.
        - DELETE /users/{id}: Deletes a specific user by ID.
        - POST /register/: Registers a new user.
        - POST /login/: Logs in a user.
        - GET /callback: Handles callback for login.
    """

    app.router.add_get('/users/', list_users)
    app.router.add_delete('/users/', clear_users)
    app.router.add_post('/users/', add_user)
    app.router.add_get('/users/{id}', show_user)
    app.router.add_patch('/users/{id}', update_user)
    app.router.add_delete('/users/{id}', remove_user)
    app.router.add_post('/register/', register_user)
    app.router.add_post('/login/', login_user) 
    app.router.add_get('/callback', handle_callback)