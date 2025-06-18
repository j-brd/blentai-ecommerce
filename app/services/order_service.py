from sqlalchemy.orm import Session
from app.models.order import Order, OrderLine, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdateStatus

def create_order(db: Session, user_id: int, order_data: OrderCreate):
    """
    Crée une commande et déduit le stock.
    """
    order = Order(user_id=user_id, delivery_address=order_data.delivery_address)
    db.add(order)
    db.flush()  # Génère l'ID de la commande

    for line_data in order_data.lines:
        product = db.query(Product).filter(Product.id == line_data.product_id).first()
        if not product or product.stock_quantity < line_data.quantity:
            raise ValueError(f"Stock insuffisant pour produit {line_data.product_id}")

        product.stock_quantity -= line_data.quantity
        order_line = OrderLine(
            order_id=order.id,
            product_id=product.id,
            quantity=line_data.quantity,
            unit_price=product.price
        )
        db.add(order_line)

    db.commit()
    db.refresh(order)
    return order

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders_for_user(db: Session, user_id: int, is_admin: bool):
    if is_admin:
        return db.query(Order).all()
    return db.query(Order).filter(Order.user_id == user_id).all()

def update_order_status(db: Session, order: Order, status: OrderStatus):
    order.status = status
    db.commit()
    db.refresh(order)
    return order
