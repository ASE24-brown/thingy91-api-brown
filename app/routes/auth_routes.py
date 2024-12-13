from auth.login import login_user, handle_callback
from app.handlers.user_handlers import register_user

def setup_auth_routes(app):
    """
    Sets up the RESTful API routes for the aiohttp application.
    
    Args:
        app (aiohttp.web.Application): The aiohttp application instance.
    Routes:
        - POST /register/: Registers a new user.
        - POST /login/: Logs in a user.
        - GET /callback: Handles callback for login.
    """
    app.router.add_post('/register/', register_user)
    app.router.add_post('/login/', login_user) 
    app.router.add_get('/callback', handle_callback)