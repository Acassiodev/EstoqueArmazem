# Em app/services/product_service.py

# ======================================================
# 1. IMPORTAÇÕES (DEVEM VIR PRIMEIRO)
# ======================================================
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

# Importe todos os módulos necessários aqui
from app.models import stock_movement_model
from app.schemas import product_schema
from app.repositories import product_repository, category_repository




def create_new_product(db: Session, product: product_schema.ProductCreate):
    """
    Serviço para criar um novo produto com validações de regras de negócio.
    """
    # REGRA: O SKU deve ser único (RF002)
    existing_product = product_repository.get_product_by_sku(db, sku=product.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )

    # REGRA: O produto deve ser vinculado a uma categoria existente (RF002)
    category = category_repository.get_category(db, category_id=product.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product.category_id} not found"
        )

    return product_repository.create_product(db=db, product=product)


def register_stock_exit(db: Session, product_id: int, quantity_to_remove: int):
    # Nota: A função get_product precisa ser criada no seu product_repository.py
    product = product_repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # REGRA DE NEGÓCIO: Não permitir estoque negativo
    if product.quantity < quantity_to_remove:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough stock. Current quantity: {product.quantity}"
        )

    # Operação Atômica: Atualiza o produto E cria o registro de movimentação
    try:
        product.quantity -= quantity_to_remove
        
        movement = stock_movement_model.StockMovement(
            product_id=product_id,
            quantity=quantity_to_remove,
            type="saida"
        )
        db.add(movement)
        
        db.commit() # Confirma as duas operações ao mesmo tempo
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback() # Desfaz tudo se houver um erro
        raise HTTPException(status_code=500, detail="An error occurred during the transaction.")
    
    

def get_product_by_id(db: Session, product_id: int):
    """
    Serviço para buscar um produto pelo ID, com tratamento de erro.
    """
    db_product = product_repository.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Adicione esta função
def update_existing_product(db: Session, product_id: int, product_update: product_schema.ProductCreate):
    product_to_update = product_repository.get_product(db, product_id)
    if not product_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Valida se a nova categoria existe
    category = category_repository.get_category(db, category_id=product_update.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {product_update.category_id} not found"
        )
        
    # Valida se o novo SKU já não está em uso por outro produto
    existing_product_with_sku = product_repository.get_product_by_sku(db, sku=product_update.sku)
    if existing_product_with_sku and existing_product_with_sku.id != product_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="SKU already in use")

    return product_repository.update_product(db, product_to_update, product_update)



def remove_product(db: Session, product_id: int):
    """
    Serviço para remover um produto pelo ID.
    """
    product_to_delete = product_repository.get_product(db, product_id)
    if not product_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    product_repository.delete_product(db, product_to_delete)
    return



def register_stock_entry(db: Session, product_id: int, movement_request: product_schema.StockMovementRequest):
    """Serviço para registrar a entrada de estoque de um produto."""
    product = product_repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    quantity_to_add = movement_request.quantity
    if quantity_to_add <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    try:
        # 1. Atualiza a quantidade no produto
        product.quantity += quantity_to_add
        
        # 2. Cria um registro no histórico de movimentações
        movement = stock_movement_model.StockMovement(
            product_id=product_id,
            quantity=quantity_to_add,
            type="entrada"
        )
        db.add(movement)
        
        db.commit() # Salva as duas alterações (produto e movimentação)
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during the stock entry transaction.")
    

    

def register_stock_exit(db: Session, product_id: int, movement_request: product_schema.StockMovementRequest):
    """Serviço para registrar a saída de estoque de um produto."""
    product = product_repository.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    quantity_to_remove = movement_request.quantity
    if quantity_to_remove <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be positive")

    # REGRA DE NEGÓCIO: Não permitir estoque negativo (RF004)
    if product.quantity < quantity_to_remove:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not enough stock. Current quantity: {product.quantity}, trying to remove: {quantity_to_remove}"
        )

    try:
        # 1. Atualiza a quantidade no produto
        product.quantity -= quantity_to_remove
        
        # 2. Cria um registro no histórico de movimentações
        movement = stock_movement_model.StockMovement(
            product_id=product_id,
            quantity=quantity_to_remove,
            type="saida"
        )
        db.add(movement)
        
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during the stock exit transaction.")
    
    