from app.core.database import Base, engine
from app.models import user, product, order

def init_db():
    """
    Crée les tables définies par les modèles SQLAlchemy si elles n'existent pas encore.
    """
    print("Initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    init_db()