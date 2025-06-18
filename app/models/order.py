from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class OrderStatus(enum.Enum):
    pending = "en_attente"
    validated = "validée"
    shipped = "expédiée"
    cancelled = "annulée"

class Order(Base):
    """
    Commande principale : contient client, adresse et statut.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    delivery_address = Column(String, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)
    
    lines = relationship("OrderLine", back_populates="order")

class OrderLine(Base):
    """
    Ligne de commande : un produit + quantité + prix unitaire.
    """
    __tablename__ = "order_lines"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="lines")
