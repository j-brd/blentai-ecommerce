from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import schemas
from app.services import user_service
from app.core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserRead)
def register(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    """
    Enregistre un nouvel utilisateur et retourne un token d'authentification JWT.
    - Vérifie si l'email est déjà utilisé.
    - Crée un utilisateur avec mot de passe haché.
    - Génère un JWT contenant l'email et le rôle.
    """
    if user_service.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    created_user = user_service.create_user(db, user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "id": created_user.id,
            "email": created_user.email,
            "full_name": created_user.full_name,
            "role": created_user.role,
        },
        headers={"Location": f"/api/users/{created_user.id}"}
    )

@router.post("/login", response_model=schemas.user.Token)
def login(credentials: schemas.user.UserLogin, db: Session = Depends(get_db)):
    """
    Authentifie un utilisateur et retourne un token d'authentification JWT.
    - Vérifie l'email et le mot de passe.
    - Génère un JWT contenant l'email et le rôle si les identifiants sont corrects.
    """
    user = user_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = user_service.create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token}