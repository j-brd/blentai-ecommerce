from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de connexion à la base de données (ici, fichier SQLite local)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app/data/pocdatabase.db"

# Création de l'engine SQLAlchemy, qui gère la connexion à la base
# connect_args est nécessaire pour SQLite en mode fichier local (single thread)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Création d'un factory pour produire des sessions DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de tous les modèles ORM (classes héritant de Base sont des tables)
Base = declarative_base()

def get_db():
    """
    Fournit une session de base de données à usage unique (dépendance FastAPI).
    
    Ouvre une session, la rend accessible à la fonction appelée,
    puis ferme la session une fois l'opération terminée.
    
    Usage :
    db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()