from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.core.config import settings
from app.core.exceptions import InvalidTokenError
import jwt

# Contexte de hachage de mot de passe
# bcrypt : algorithme robuste pour le hachage sécurisé des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt_token(data: dict):
    """
    Génère un token JWT signé contenant les données fournies + date d'expiration.

    Args:
        data (dict): Données à inclure dans le token (ex : {"sub": email, "role": role}).
        settings: Objet contenant la configuration (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns:
        str: Le JWT encodé sous forme de string.
    """

    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_and_verify_jwt(token: str) -> dict:
    """
    Décode et valide un JWT signé.
    Retourne le payload si valide.
    """
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError:
        raise InvalidTokenError("Token invalide")