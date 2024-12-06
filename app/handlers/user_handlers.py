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
    ---
    summary: Register a new user
    description: Handle user registration.
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              password:
                type: string
              email:
                type: string
    responses:
      '201':
        description: User registered successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      '400':
        description: Missing required fields or user already exists
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
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
    ---
    description: Retrieve a list of all users.
    tags:
        - Users
    responses:
        "200":
            description: Successful response
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            type: object
                            properties:
                                id:
                                    type: integer
                                    description: User ID
                                username:
                                    type: string
                                    description: Username
                                email:
                                    type: string
                                    description: Email address
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
    ---
    summary: Delete all users
    description: Delete all users from the database.
    tags:
      - Users
    responses:
      '204':
        description: Users deleted successfully
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
    ---
    summary: Add a new user
    description: Add a new user to the database.
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
    responses:
      '201':
        description: User created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
      '400':
        description: Username and email are required or email already registered
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
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
    ---
    summary: Retrieve a user by ID
    description: Retrieve a user's details from the database by their ID.
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '200':
        description: A user object
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
      '404':
        description: User not found
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
    ---
    summary: Update a user's details
    description: Update a user's details in the database.
    tags:
      - Users
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
            type: object
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
    responses:
      '200':
        description: User updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
      '404':
        description: User not found
      '500':
        description: Internal server error
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
    ---
    summary: Delete a user by ID
    description: Delete a user from the database by their ID.
    tags:
      - Users
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '204':
        description: User deleted successfully
      '404':
        description: User not found
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