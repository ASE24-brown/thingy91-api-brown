from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal

import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# CRUD operations for User

# curl -X GET http://localhost:8080/users/
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


# curl -X DELETE http://localhost:8080/users/
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


# curl -X POST http://localhost:8080/users/ -H "Content-Type: application/json" -d '{"username": "johndoe", "email": "johndoe@example.com"}'
async def add_user(request):
    """
    Add a new user to the database.

    :param request: The HTTP request object containing user data.
    :return: JSON response with the created user's details or an error message.
    """
    data = await request.json()
    username = data.get('username')
    email = data.get('email')
    #name = data.get('name')
    #description = data.get('description')
    #type = data.get('type')

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


# curl -X GET http://localhost:8080/users/1 
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


# curl -X PATCH http://localhost:8080/users/1 -H "Content-Type: application/json" -d '{"username": "johnsmith", "email": "johnsmith@example.com"}'
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

# curl -X DELETE http://localhost:8080/users/1
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


# CRUD operations for Profile
#curl -X GET http://localhost:8080/profiles/
async def list_profiles(request):
    """
    Retrieves a list of all profiles.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing a list of profiles.
    """
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(Profile))
            profiles = result.scalars().all()
            return web.json_response([{
                "id": profile.id,
                "name": profile.name,
                "description": profile.description,
                "type": profile.type,
                "level": profile.level
            } for profile in profiles])

#curl -X DELETE http://localhost:8080/profiles/
async def clear_profiles(request):
    """
    Deletes all profiles.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: Response with status 204 (No Content).
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Profile))
            await session.commit()
            return web.Response(status=204)

# curl -X POST http://localhost:8080/profiles/ -H "Content-Type: application/json" -d '{"name": "Admin", "description": "Administrator profile", "type": "admin", "user_id": 1}'
async def add_profile(request):
    """
    Creates a new profile.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the created profile.
    """
    data = await request.json()
    name = data.get('name')
    description = data.get('description')
    type = data.get('type')
    user_id = data.get('user_id')

    async with SessionLocal() as session:
        try:
            profile = Profile(name=name, description=description, type=type, user_id=user_id)
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
            return web.json_response({
                "id": profile.id,
                "name": profile.name,
                "description": profile.description,
                "type": profile.type,
                "user_id": profile.user_id
            }, status=201)
        except IntegrityError:
            await session.rollback()
            return web.json_response({"error": "Integrity constraint violated. Failed to add profile."}, status=400)
        except Exception as e:
            await session.rollback()
            return web.json_response({"error": str(e)}, status=500)

# curl -X GET http://localhost:8080/profiles/1    
async def show_profile(request):
    """
    Retrieves a specific profile by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the profile.
    """
    profile_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            profile = await session.get(Profile, profile_id)
            if not profile:
                raise web.HTTPNotFound(reason='Profile not found')
            return web.json_response({
                "id": profile.id,
                "name": profile.name,
                "description": profile.description,
                "type": profile.type,
                "user_id": profile.user_id
            })

# curl -X PATCH http://localhost:8080/profiles/1 -H "Content-Type: application/json" -d '{"name": "User", "description": "User profile", "type": "user"}'
async def update_profile(request):
    """
    Updates a specific profile by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: JSON response containing the updated profile.
    """
    profile_id = request.match_info['id']
    data = await request.json()

    async with SessionLocal() as session:
        #async with session.begin():
            profile = await session.get(Profile, profile_id)
            if not profile:
                raise web.HTTPNotFound(reason='Profile not found')
            
            for key, value in data.items():
                setattr(profile, key, value)

            await session.commit()
            await session.refresh(profile)
            return web.json_response({
                "id": profile.id,
                "name": profile.name,
                "description": profile.description,
                "type": profile.type,
                "user_id": profile.user_id
            })

# curl -X DELETE http://localhost:8080/profiles/1
async def remove_profile(request):
    """
    Deletes a specific profile by ID.

    Args:
        request (aiohttp.web.Request): The request object.

    Returns:
        aiohttp.web.Response: Response with status 204 (No Content).
    """
    profile_id = request.match_info['id']
    async with SessionLocal() as session:
        async with session.begin():
            profile = await session.get(Profile, profile_id)
            if not profile:
                raise web.HTTPNotFound(reason='Profile not found')
            await session.delete(profile)
            await session.commit()
            return web.Response(status=204)