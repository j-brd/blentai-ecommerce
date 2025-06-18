from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schéma utilisé pour l'inscription d'un utilisateur.
    """
    email: EmailStr
    password: str
    full_name: str
    role: Literal["client", "admin"]  # Seules ces valeurs sont acceptées

class UserLogin(BaseModel):
    """
    Schéma utilisé pour la connexion d'un utilisateur.
    """
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None
    role: Literal["client", "admin"]
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Schéma de la réponse retournée après inscription ou connexion.
    """
    access_token: str
    token_type: str = "bearer"
