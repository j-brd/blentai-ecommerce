from pydantic import BaseModel
from typing import List, Literal, Optional
from datetime import datetime
from app.models.order import OrderStatus

class OrderLineCreate(BaseModel):
    """
    Données nécessaires pour ajouter un produit à une commande.
    """
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    """
    Données nécessaires pour créer une commande complète.
    """
    delivery_address: str
    lines: List[OrderLineCreate]

class OrderLineRead(BaseModel):
    """
    Données retournées pour une ligne de commande.
    """
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True

class OrderRead(BaseModel):
    """
    Données retournées pour une commande complète.
    """
    id: int
    delivery_address: str
    status: OrderStatus
    lines: List[OrderLineRead]
    created_at: datetime

    class Config:
        orm_mode = True
        use_enum_values = True

class OrderUpdateStatus(BaseModel):
    """
    Données nécessaires pour mettre à jour le statut d'une commande.
    """
    status: OrderStatus
