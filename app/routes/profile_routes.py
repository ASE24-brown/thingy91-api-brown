from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.sql.expression import delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.models import User, Profile, SensorData
from app.extensions import SessionLocal


def setup_profile_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /profiles/: Retrieves a list of all profiles.
        DELETE /profiles/: Deletes all profiles.
        POST /profiles/: Creates a new profile.
        GET /profiles/{id}: Retrieves a specific profile by ID.
        PATCH /profiles/{id}: Updates a specific profile by ID.
        DELETE /profiles/{id}: Deletes a specific profile by ID.
    """
   
    app.router.add_get('/profiles/', list_profiles)
    app.router.add_delete('/profiles/', clear_profiles)
    app.router.add_post('/profiles/', add_profile)
    app.router.add_get('/profiles/{id}', show_profile)
    app.router.add_patch('/profiles/{id}', update_profile)
    app.router.add_delete('/profiles/{id}', remove_profile)
    
# CRUD operations for Profile
#curl -X GET http://localhost:8000/profiles/
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

#curl -X DELETE http://localhost:8000/profiles/
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

# curl -X POST http://localhost:8000/profiles/ -H "Content-Type: application/json" -d '{"name": "Admin", "description": "Administrator profile", "type": "admin", "user_id": 1}'
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

# curl -X GET http://localhost:8000/profiles/1    
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
    