from flask import Blueprint
from .handlers import authorize, token

oauth_bp = Blueprint('oauth', __name__)

oauth_bp.route('/oauth/authorize', methods=['GET', 'POST'])(authorize)
oauth_bp.route('/oauth/token', methods=['POST'])(token)