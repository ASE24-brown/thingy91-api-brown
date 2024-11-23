from sqlalchemy.orm import Session
from app.models import User
import bcrypt

def authenticate_user(session: Session, username: str, plain_password: str):
    """
    Authenticate a user by verifying their username and password.

    :param session: SQLAlchemy session object.
    :param username: The username to look up.
    :param plain_password: The plaintext password provided by the user.
    :return: The authenticated user object if successful, None otherwise.
    """
    # Rechercher l'utilisateur dans la base de données
    user = session.query(User).filter(User.username == username).first()

    # Vérifier que l'utilisateur existe et que le mot de passe correspond
    if user and bcrypt.checkpw(plain_password.encode('utf-8'), user.password.encode('utf-8')):
        return user  # Authentifié avec succès
    return None  # Échec de l'authentification
