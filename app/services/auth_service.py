from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from app.core.config import settings
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_email
from app.core.security import decode_and_verify_jwt
from app.core.exceptions import InvalidTokenError, UserNotFoundError

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),db: Session = Depends(get_db)):
    """
    Valide le token, vérifie que l'utilisateur existe encore.
    """
    token = credentials.credentials
    payload = decode_and_verify_jwt(token)

    email = payload.get("sub")
    if not email:
        raise InvalidTokenError("Token invalide : sub manquant")

    user = get_user_by_email(db, email)
    if not user:
        raise UserNotFoundError("Utilisateur inexistant")

    return user