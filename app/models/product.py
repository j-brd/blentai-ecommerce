from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Product(Base):
    """
    Modèle produit avec gestion du stock en quantité.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, nullable=False, default=0)