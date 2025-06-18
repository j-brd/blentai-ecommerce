from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas import order as order_schemas
from app.services import order_service
from app.services.permissions import require_role
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/commandes", tags=["Commandes"])

@router.post("/", response_model=order_schemas.OrderRead)
def create_order(
    order: order_schemas.OrderCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    """
    Crée une nouvelle commande pour l'utilisateur connecté.
    Vérifie les stocks et met à jour les quantités.
    """
    try:
        return order_service.create_order(db, user.id, order)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=List[order_schemas.OrderRead])
def list_orders( db: Session = Depends(get_db),user = Depends(get_current_user)):
    """
    Liste les commandes de l'utilisateur connecté ou toutes les commandes si admin.
    """
    is_admin = user.role == "admin"
    return order_service.get_orders_for_user(db, user.id, is_admin)

@router.get("/{order_id}", response_model=order_schemas.OrderRead)
def get_order( order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    """
    Récupère une commande par son ID.
    Le client ne peut voir que ses propres commandes.
    """
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(404, "Commande non trouvée")
    if user.role != "admin" and order.user_id != user.id:
        raise HTTPException(404, "Commande non trouvée")
    return order

@router.patch("/{order_id}", response_model=order_schemas.OrderRead, dependencies=[Depends(require_role("admin"))])
def update_order_status( order_id: int, status: order_schemas.OrderUpdateStatus,db: Session = Depends(get_db)):
    """
    Met à jour le statut d'une commande (admin uniquement).
    """
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(404, "Commande non trouvée")
    return order_service.update_order_status(db, order, status.status)

@router.get("/{order_id}/lignes", response_model=List[order_schemas.OrderLineRead])
def get_order_lines( order_id: int, db: Session = Depends(get_db),user = Depends(get_current_user)):
    """
    Retourne les lignes d'une commande.
    Le client ne voit que ses propres commandes.
    """
    order = order_service.get_order(db, order_id)
    if not order:
        raise HTTPException(404, "Commande non trouvée")
    if user.role != "admin" and order.user_id != user.id:
        raise HTTPException(404, "Commande non trouvée")
    return order.lines
