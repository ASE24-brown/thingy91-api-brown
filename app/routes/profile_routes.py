from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData
from app.handlers.profile_handlers import list_profiles, clear_profiles, add_profile, show_profile, update_profile, remove_profile

def setup_profile_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application with OpenAPI-compatible documentation for aiohttp-swagger.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        - GET /profiles/: Retrieves a list of all profiles.
        - DELETE /profiles/: Deletes all profiles.
        - POST /profiles/: Creates a new profile.
        - GET /profiles/{id}: Retrieves a specific profile by ID.
        - PATCH /profiles/{id}: Updates a specific profile by ID.
        - DELETE /profiles/{id}: Deletes a specific profile by ID.
    """
   
    app.router.add_get('/profiles/', list_profiles)
    app.router.add_delete('/profiles/', clear_profiles)
    app.router.add_post('/profiles/', add_profile)
    app.router.add_get('/profiles/{id}', show_profile)
    app.router.add_patch('/profiles/{id}', update_profile)
    app.router.add_delete('/profiles/{id}', remove_profile)