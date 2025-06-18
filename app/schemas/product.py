from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    """
    Schéma de base commun aux opérations sur un produit.
    Contient les champs principaux partagés entre création, lecture et mise à jour.
    """
    name: str               # Nom du produit
    description: str        # Description détaillée du produit
    category: str           # Catégorie à laquelle appartient le produit
    price: float            # Prix unitaire du produit
    stock_quantity: int     # Quantité disponible en stock

class ProductCreate(ProductBase):
    """
    Schéma utilisé lors de la création d'un produit.
    Hérite de tous les champs de ProductBase.
    """
    pass

class ProductUpdate(BaseModel):
    """
    Schéma utilisé lors de la mise à jour partielle d'un produit.
    Tous les champs sont facultatifs : seuls ceux fournis seront mis à jour.
    """
    name: Optional[str]
    description: Optional[str]
    category: Optional[str]
    price: Optional[float]
    stock_quantity: Optional[int]

class ProductRead(ProductBase):
    """
    Schéma utilisé pour la lecture d'un produit.
    Inclut l'ID unique du produit en plus des champs de base.
    """
    id: int  # Identifiant unique du produit
    created_at: datetime

    class Config:
        orm_mode = True  # Permet la conversion ORM → Pydantic directement
