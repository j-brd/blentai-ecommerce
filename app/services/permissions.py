from fastapi import Depends, HTTPException, status
from app.services import auth_service

def require_role(required_role: str):
    """
    Génère une dépendance qui vérifie le rôle requis.
    """
    def dependency(user = Depends(auth_service.get_current_user)):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès réservé au rôle {required_role}"
            )
        return user
    return dependency