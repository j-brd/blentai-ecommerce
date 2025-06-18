from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app import schemas
from app.services import product_service
from app.services.permissions import require_role

router = APIRouter(prefix="/api/produits", tags=["Produits"])

@router.get("/", response_model=List[schemas.product.ProductRead])
def list_products(db: Session = Depends(get_db), search: str = Query(None)):
    """
    Liste ou recherche les produits.
    """
    if search:
        return product_service.search_products(db, search)
    return product_service.get_all_products(db)

@router.get("/{product_id}", response_model=schemas.product.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Récupère un produit par ID.
    """
    product = product_service.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

@router.post("/", response_model=schemas.product.ProductRead, status_code=201, dependencies=[Depends(require_role("admin"))])
def create_product(product: schemas.product.ProductCreate, db: Session = Depends(get_db)):
    """
    Crée un produit (admin uniquement).
    """
    return product_service.create_product(db, product)

@router.put("/{product_id}", response_model=schemas.product.ProductRead,dependencies=[Depends(require_role("admin"))])
def update_product(product_id: int, updates: schemas.product.ProductUpdate, db: Session = Depends(get_db)):
    """
    Modifie un produit (admin uniquement).
    """
    db_product = product_service.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product_service.update_product(db, db_product, updates)

@router.delete("/{product_id}", status_code=204,dependencies=[Depends(require_role("admin"))])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Supprime un produit (admin uniquement).
    """
    db_product = product_service.get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    product_service.delete_product(db, db_product)
    return