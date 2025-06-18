from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

# Contexte de hachage de mot de passe
# bcrypt : algorithme robuste pour le hachage sécurisé des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_jwt_token(data: dict, settings):
    """
    Génère un token JWT signé contenant les données fournies + date d'expiration.

    Args:
        data (dict): Données à inclure dans le token (ex : {"sub": email, "role": role}).
        settings: Objet contenant la configuration (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES).

    Returns:
        str: Le JWT encodé sous forme de string.
    """
    # Copie des données à encoder dans le token
    to_encode = data.copy()

    # Calcul de la date d'expiration (UTC)
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Ajout de l'expiration au payload
    to_encode.update({"exp": expire})

    # Génération du token signé
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
