import os
from dotenv import load_dotenv

# Charge .env (si présent)
load_dotenv()

class Settings:
    """
    Configuration centralisée de l'application.
    Variables d'environnement actives (ex : export SECRET_KEY=xxx ou via lancement)
    1 - Variables d'environnement actives
    2 - Valeurs du fichier .env
    3 - Valeurs par défaut hardcodées
    """
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeit")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()