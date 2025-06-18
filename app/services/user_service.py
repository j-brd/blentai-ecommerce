from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import pwd_context, create_jwt_token
from app.schemas.user import UserCreate
from app.core.config import settings

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: UserCreate):
    """
    Crée un nouvel utilisateur avec un mot de passe haché et l'enregistre en base.
    """
    hashed_password = pwd_context.hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Vérifie les identifiants d'un utilisateur (email + mot de passe).
    """
    user = get_user_by_email(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict):
    """
    Génère un JWT signé contenant les données fournies + une date d'expiration.
    """
    return create_jwt_token(data, settings)
