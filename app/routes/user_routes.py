from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal
from services.user_service import authenticate_user
import bcrypt
import logging
from auth.auth import generate_access_token

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def setup_user_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /users/: Retrieves a list of all users.
        DELETE /users/: Deletes all users.
        POST /users/: Creates a new user with a profile.
        GET /users/{id}: Retrieves a specific user by ID.
        PATCH /users/{id}: Updates a specific user by ID.
        DELETE /users/{id}: Deletes a specific user by ID.
    """

    app.router.add_get('/users/', list_users)
    app.router.add_delete('/users/', clear_users)
    app.router.add_post('/users/', add_user)
    app.router.add_get('/users/{id}', show_user)
    app.router.add_patch('/users/{id}', update_user)
    app.router.add_delete('/users/{id}', remove_user)
    app.router.add_post('/login/', login_user) 
    
# CRUD operations for User
# curl -X GET http://localhost:8000/users/
# curl.exe -X GET http://localhost:8080/users/
async def list_users(request):
    """
    List all users in the database.

    :param request: The HTTP request object.
    :return: JSON response containing a list of users.
    """
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User.id, User.username, User.email))
            users = result.scalars().all()
            return web.json_response([{"id": user.id, "username": user.username, "email": user.email} for user in users])

# curl.exe -X DELETE http://localhost:8000/users/
async def clear_users(request):
    """
    Delete all users from the database.

    :param request: The HTTP request object.
    :return: HTTP response with status 204 (No Content).
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(User))
            await session.commit()
            return web.Response(status=204)

# curl -X POST http://localhost:8000/users/ -H "Content-Type: application/json" -d '{"username": "johndoe", "email": "johndoe@example.com"}'
async def add_user(request):
    """
    Add a new user to the database.

    :param request: The HTTP request object containing user data.
    :return: JSON response with the created user's details or an error message.
    """
    data = await request.json()
    username = data.get('username')
    email = data.get('email')
    plain_password = data.get('password')
    #name = data.get('name')
    #description = data.get('description')
    #type = data.get('type')

    logger.debug(f"Received data: {data}")

    # Validate required fields
    if not username or not email or not plain_password:
        return web.json_response({"error": "Username and email are required"}, status=400)
    
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    async with SessionLocal() as session:
        async with session.begin():
            # Check if a user with the given email already exists
            existing_user = await session.execute(
                select(User).filter_by(email=email)
            )
            if existing_user.scalars().first():
                logger.debug("Email already registered")
                return web.json_response({"error": "Email already registered"}, status=400)

            try:
                user = User(username=username, email=email, password=hashed_password)
                session.add(user)
                await session.flush()

                # Access user.id before the session is closed
                user_id = user.id

                # Optionally create a Profile if additional fields are provided
                #if name or description or type:
                #    profile = Profile(name=name, description=description, type=type, user_id=user.id)
                #    session.add(profile)

                await session.commit()
                logger.debug(f"User created with ID: {user_id}")

                return web.json_response({"id": user_id, "username": username, "email": email}, status=201)

            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                await session.rollback()
                return web.json_response({"error": "Failed to create user"}, status=400)
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                await session.rollback()
                return web.json_response({"error": "Failed to create user"}, status=400)

# curl -X GET http://localhost:8000/users/1 
async def show_user(request):
    """
    Retrieve a user by ID.

    :param request: The HTTP request object.
    :return: JSON response with the user's details or an error message.
    """
    user_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                raise web.HTTPNotFound(reason='User not found')
            return web.json_response({
                "id": user.id,
                "username": user.username,
                "email": user.email
            })

# curl -X PATCH http://localhost:8000/users/1 -H "Content-Type: application/json" -d '{"username": "johnsmith", "email": "johnsmith@example.com"}'
async def update_user(request):
    """
    Update a user's details.

    :param request: The HTTP request object containing updated user data.
    :return: JSON response with the updated user's details or an error message.
    """
    user_id = request.match_info['id']
    data = await request.json()

    async with SessionLocal() as session:
        # Retrieve the user from the database
        user = await session.get(User, user_id)
        if not user:
            raise web.HTTPNotFound(reason='User not found')

        # Update the user's attributes
        for key, value in data.items():
            setattr(user, key, value)

        # Commit and refresh within the same context
        try:
            await session.commit()  # Commit the changes
            await session.refresh(user)  # Refresh the user instance
        except Exception as e:
            await session.rollback()
            raise web.HTTPInternalServerError(reason=str(e))

        # Return the updated user data
        return web.json_response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

# curl -X DELETE http://localhost:8000/users/1
async def remove_user(request):
    """
    Delete a user by ID.

    :param request: The HTTP request object.
    :return: HTTP response with status 204 (No Content) or an error message.
    """
    user_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if not user:
                raise web.HTTPNotFound(reason='User not found')
            await session.delete(user)
            await session.commit()
            return web.Response(status=204)


async def login_user(request):
    """
    Handle user login requests.

    :param request: The HTTP request object containing login credentials.
    :return: JSON response indicating success or failure.
    """
    data = await request.json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return web.json_response({"error": "Username and password are required"}, status=400)

    async with SessionLocal() as session:
        user = authenticate_user(session, username, password)
        if user:
            # Exemple de réponse : créer un token ou retourner les infos utilisateur
            #return web.json_response({"message": "Login successful", "user_id": user.id}, status=200)
        
            # Génération d'un token d'accès OAuth2 ou JWT
            token = generate_access_token(user)
            return web.json_response({"access_token": token, "token_type": "Bearer"}, status=200)
        else:
            return web.json_response({"error": "Invalid credentials"}, status=401)
        
        