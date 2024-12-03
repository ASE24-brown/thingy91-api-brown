from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal


async def list_profiles(request):
    """
    ---
    summary: Retrieve a list of all profiles
    description: Retrieves a list of all profiles from the database.
    tags:
      - Profiles
    responses:
      '200':
        description: A list of profiles
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  description:
                    type: string
                  type:
                    type: string
                  level:
                    type: string
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

async def clear_profiles(request):
    """
    ---
    summary: Delete all profiles
    description: Deletes all profiles from the database.
    tags:
      - Profiles
    responses:
      '204':
        description: Profiles deleted successfully
    """
    async with SessionLocal() as session:
        async with session.begin():
            await session.execute(delete(Profile))
            await session.commit()
            return web.Response(status=204)

async def add_profile(request):
    """
    ---
    summary: Create a new profile
    description: Creates a new profile in the database.
    tags:
      - Profiles
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                description: Name of the profile
              description:
                type: string
                description: Description of the profile
              type:
                type: string
                description: Type of the profile
              user_id:
                type: integer
                description: ID of the user associated with the profile
    responses:
      '201':
        description: Profile created successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                type:
                  type: string
                user_id:
                  type: integer
      '400':
        description: Integrity constraint violated. Failed to add profile.
      '500':
        description: Internal server error
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

  
async def show_profile(request):
    """
    ---
    summary: Retrieve a specific profile by ID
    description: Retrieves a specific profile from the database by its ID.
    tags:
      - Profiles
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '200':
        description: A profile object
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                type:
                  type: string
                user_id:
                  type: integer
      '404':
        description: Profile not found
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

async def update_profile(request):
    """
    ---
    summary: Update a specific profile by ID
    description: Updates a specific profile in the database by its ID.
    tags:
      - Profiles
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
              name:
                type: string
              description:
                type: string
              type:
                type: string
              user_id:
                type: integer
    responses:
      '200':
        description: Profile updated successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
                type:
                  type: string
                user_id:
                  type: integer
      '404':
        description: Profile not found
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

async def remove_profile(request):
    """
    ---
    summary: Delete a specific profile by ID
    description: Deletes a specific profile from the database by its ID.
    tags:
      - Profiles
    parameters:
      - in: path
        name: id
        required: true
        schema:
          type: string
    responses:
      '204':
        description: Profile deleted successfully
      '404':
        description: Profile not found
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
    