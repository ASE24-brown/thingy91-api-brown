from app.control.user_controller import list_users, clear_users, add_user, show_user, update_user, remove_user, get_user_id_by_username

def setup_user_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.

    Args:
        app (aiohttp.web.Application): The aiohttp application instance.

    Routes:
        - GET /users/: Retrieves a list of all users.
        - DELETE /users/: Deletes all users.
        - POST /users/: Creates a new user with a profile.
        - GET /users/{id}: Retrieves a specific user by ID.
        - PATCH /users/{id}: Updates a specific user by ID.
        - DELETE /users/{id}: Deletes a specific user by ID.
        - GET /users/get_id: Retrieves the user ID by username.
    """

    app.router.add_get('/users/', list_users)
    app.router.add_delete('/users/', clear_users)
    app.router.add_post('/users/', add_user)
    app.router.add_get('/users/{id}', show_user)
    app.router.add_patch('/users/{id}', update_user)
    app.router.add_delete('/users/{id}', remove_user)
    app.router.add_get('/users/get_id', get_user_id_by_username)
