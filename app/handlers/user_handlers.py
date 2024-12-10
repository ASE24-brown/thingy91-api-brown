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
from auth.login import login_user


async def register_user(request):
    """
    Handle user registration.
    
    params:
      request: The request object containing user data.
    return:
      A JSON response indicating success or failure of user registration.
    """
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return web.json_response({"error": "Missing required fields"}, status=400)

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    async with SessionLocal() as session:
        async with session.begin():
            new_user = User(username=username, password=hashed_password, email=email)
            session.add(new_user)
            try:
                await session.commit()
                return web.json_response({"message": "User registered successfully"}, status=201)
            except IntegrityError:
                await session.rollback()
                return web.json_response({"error": "User already exists"}, status=400)

async def list_users(request):
    """
    Retrieve a list of all users.

    params:
        request: The request object.
    return:
        A JSON response containing a list of users.
    """
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User))
            users = result.scalars().all()

            return web.json_response([{"id": user.id, "username": user.username, "email": user.email} for user in users])

async def clear_users(request):
    """
    Delete all users from the database.

    params:
      request: The request object.
    return:
      A response indicating the success of the operation.
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(User))
            await session.commit()
            return web.Response(status=204)

async def add_user(request):
    """
    Add a new user to the database.
    
    params:
      request: The request object containing user data.
    return:
      A JSON response indicating success or failure of user creation.
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
    Retrieve a user's details from the database by their ID.
    
    params:
      request: The request object containing the user ID.
    return:
      A JSON response with the user's details or a 404 error if the user is not found.
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
    Update a user's details in the database.
    
    params:
      request: The request object containing user data.
    return:
      A JSON response with the updated user details or an error message.
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
    Delete a user from the database by their ID.
    
    params:
      request: The request object containing the user ID.
    return:
      A response indicating the success of the operation or an error message.
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