from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import stock_movement_repository, product_repository

def get_product_movement_history(db: Session, product_id: int):
    """
    Serviço para buscar o histórico de movimentações de um produto.
    """
    # Primeiro, verifica se o produto existe
    product = product_repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Se o produto existe, busca seu histórico
    history = stock_movement_repository.get_movements_by_product_id(db, product_id=product_id)
    return history