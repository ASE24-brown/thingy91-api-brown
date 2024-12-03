from sqlalchemy.exc import IntegrityError
from app.models import User, Profile, SensorData
from app.handlers.profile_handlers import list_profiles, clear_profiles, add_profile, show_profile, update_profile, remove_profile

def setup_profile_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application with OpenAPI-compatible documentation for aiohttp-swagger.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        GET /profiles/:
            summary: Retrieves a list of all profiles.
            responses:
                200:
                    description: A list of profiles.
        DELETE /profiles/:
            summary: Deletes all profiles.
            responses:
                204:
                    description: Profiles deleted successfully.
        POST /profiles/:
            summary: Creates a new profile.
            requestBody:
                required: true
                content:
                    application/json:
                        schema:
                            $ref: '#/components/schemas/Profile'
            responses:
                201:
                    description: Profile created successfully.
        GET /profiles/{id}:
            summary: Retrieves a specific profile by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                200:
                    description: A profile object.
                404:
                    description: Profile not found.
        PATCH /profiles/{id}:
            summary: Updates a specific profile by ID.
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
                            $ref: '#/components/schemas/Profile'
            responses:
                200:
                    description: Profile updated successfully.
                404:
                    description: Profile not found.
        DELETE /profiles/{id}:
            summary: Deletes a specific profile by ID.
            parameters:
                - in: path
                  name: id
                  required: true
                  schema:
                      type: string
            responses:
                204:
                    description: Profile deleted successfully.
                404:
                    description: Profile not found.
    """
   
    app.router.add_get('/profiles/', list_profiles)
    app.router.add_delete('/profiles/', clear_profiles)
    app.router.add_post('/profiles/', add_profile)
    app.router.add_get('/profiles/{id}', show_profile)
    app.router.add_patch('/profiles/{id}', update_profile)
    app.router.add_delete('/profiles/{id}', remove_profile)