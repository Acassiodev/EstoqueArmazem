from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/")
def read_products():
    return [{"product_name": "Produto Exemplo 1"}, {"product_name": "Produto Exemplo 2"}]



from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import product_schema
from app.services import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# RF002 - Criar produto com SKU único
@router.post("/", response_model=product_schema.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.create_new_product(db=db, product=product)




# RF002 - Buscar produto por ID
@router.get("/{product_id}", response_model=product_schema.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = product_service.get_product_by_id(db, product_id=product_id)
    return product

# Adicione este endpoint
@router.put("/{product_id}", response_model=product_schema.Product)
def update_product(product_id: int, product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    return product_service.update_existing_product(db, product_id, product)



# RF002 - Excluir produto
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product_service.remove_product(db, product_id=product_id)
    return



# RF003 - Registrar entrada de mercadorias
@router.post("/{product_id}/entry", response_model=product_schema.Product)
def add_stock(product_id: int, movement: product_schema.StockMovementRequest, db: Session = Depends(get_db)):
    return product_service.register_stock_entry(db, product_id, movement)


# RF003 - Registrar saída de mercadorias
@router.post("/{product_id}/exit", response_model=product_schema.Product)
def remove_stock(product_id: int, movement: product_schema.StockMovementRequest, db: Session = Depends(get_db)):
    return product_service.register_stock_exit(db, product_id, movement)


# Em app/routers/product_router.py
from app.schemas import stock_movement_schema 
from app.services import stock_movement_service 



# RF003 - Histórico de movimentações (entrada/saída)
@router.get("/{product_id}/history", response_model=List[stock_movement_schema.StockMovement])
def read_product_history(product_id: int, db: Session = Depends(get_db)):
    history = stock_movement_service.get_product_movement_history(db, product_id=product_id)
    return history