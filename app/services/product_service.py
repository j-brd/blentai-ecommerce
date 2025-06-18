from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_all_products(db: Session):
    """
    Retourne tous les produits du catalogue.
    """
    return db.query(Product).all()

def get_product(db: Session, product_id: int):
    """
    Retourne un produit par son ID ou None s'il n'existe pas.
    """
    return db.query(Product).filter(Product.id == product_id).first()

def search_products(db: Session, query: str):
    """
    Recherche des produits dont le nom contient la chaîne donnée (insensible à la casse).
    """
    return db.query(Product).filter(Product.name.ilike(f"%{query}%")).all()

def create_product(db: Session, product_data: ProductCreate):
    """
    Crée et persiste un nouveau produit en base.
    """
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product: Product, updates: ProductUpdate):
    """
    Met à jour un produit existant avec les champs fournis.
    Seuls les champs précisés dans updates sont modifiés.
    """
    # Applique les champs présents dans updates (exclude_unset évite d'écraser inutilement)
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product: Product):
    """
    Supprime un produit existant de la base.
    """
    db.delete(product)
    db.commit()
