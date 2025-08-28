
from sqlalchemy.orm import Session
from app.models import product_model
from app.schemas import product_schema

def get_product_by_sku(db: Session, sku: str):
    """Busca um produto pelo seu SKU."""
    return db.query(product_model.Product).filter(product_model.Product.sku == sku).first()

def create_product(db: Session, product: product_schema.ProductCreate):
    """Cria um novo produto no banco de dados."""
    # O estoque inicial é 0, conforme o requisito RF003
    db_product = product_model.Product(
        sku=product.sku,
        name=product.name,
        description=product.description,
        category_id=product.category_id,
        quantity=0 
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



def get_product(db: Session, product_id: int):
    """Busca um produto pelo seu ID."""
    return db.query(product_model.Product).filter(product_model.Product.id == product_id).first()


# Adicione esta função
def update_product(db: Session, product: product_model.Product, update_data: product_schema.ProductCreate):
    product.sku = update_data.sku
    product.name = update_data.name
    product.description = update_data.description
    product.category_id = update_data.category_id
    db.commit()
    db.refresh(product)
    return product



def delete_product(db: Session, product: product_model.Product):
    """Exclui um produto do banco de dados."""
    db.delete(product)
    db.commit()

    