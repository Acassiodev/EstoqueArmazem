from sqlalchemy.orm import Session
from app.models import stock_movement_model

def get_movements_by_product_id(db: Session, product_id: int):
    """Busca o histórico de movimentações de um produto específico, ordenado pela data mais recente."""
    return db.query(stock_movement_model.StockMovement).filter(
        stock_movement_model.StockMovement.product_id == product_id
    ).order_by(stock_movement_model.StockMovement.timestamp.desc()).all()