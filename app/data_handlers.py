from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, UserProfile, SensorData
from app.extensions import SessionLocal

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# CRUD operations for User

async def list_users(request):
    """
    List all users in the database.

    :param request: The HTTP request object.
    :return: JSON response containing a list of users.
    """
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()
            return web.json_response([{"id": user.id, "username": user.username, "email": user.email} for user in users])

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
        
async def add_user(request):
    """
    Add a new user to the database.

    :param request: The HTTP request object containing user data.
    :return: JSON response with the created user's details or an error message.
    """
    data = await request.json()
    username = data.get('username')
    email = data.get('email')
    full_name = data.get('full_name')
    bio = data.get('bio')
    avatar_url = data.get('avatar_url')

    logger.debug(f"Received data: {data}")

    # Validate required fields
    if not username or not email:
        return web.json_response({"error": "Username and email are required"}, status=400)

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
                user = User(username=username, email=email)
                session.add(user)
                await session.flush()

                # Access user.id before the session is closed
                user_id = user.id

                # Optionally create a UserProfile if additional fields are provided
                if full_name or bio or avatar_url:
                    profile = UserProfile(full_name=full_name, bio=bio, avatar_url=avatar_url, user_id=user.id)
                    session.add(profile)

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



async def get_sensor_data(request):
    async with SessionLocal() as db:  # Use async context manager
        # Use an async query to fetch all sensor data
        result = await db.execute(select(SensorData))
        data = result.scalars().all()
        
        sensor_data = [
            {
                "id": sensor.id,
                "appId": sensor.appId,
                "data": sensor.data,
                "messageType": sensor.messageType,
                "timestamp": sensor.ts
            }
            for sensor in data
        ]
        return web.json_response({"sensor_data": sensor_data})