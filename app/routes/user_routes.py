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
        GET /users/:
            summary: Retrieves a list of all users.
            responses:
                200:
                    description: A list of users.
        DELETE /users/:
            summary: Deletes all users.
            responses:
                204:
                    description: Users deleted successfully.
        POST /users/:
            summary: Creates a new user with a profile.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/User'
            responses:
                201:
                    description: User created successfully.
        GET /users/{id}:
            summary: Retrieves a specific user by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                200:
                    description: A user object.
                404:
                    description: User not found.
        PATCH /users/{id}:
            summary: Updates a specific user by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/User'
            responses:
                200:
                    description: User updated successfully.
                404:
                    description: User not found.
        DELETE /users/{id}:
            summary: Deletes a specific user by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                204:
                    description: User deleted successfully.
                404:
                    description: User not found.
        POST /register/:
            summary: Registers a new user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/User'
            responses:
                201:
                    description: User registered successfully.
        POST /login/:
            summary: Logs in a user.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Login'
            responses:
                200:
                    description: User logged in successfully.
                401:
                    description: Invalid credentials.
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